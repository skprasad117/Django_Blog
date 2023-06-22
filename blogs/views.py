from django.shortcuts import render, HttpResponse
from . forms import CustomUserForm, PostEditorForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm
import sys
import os
from . logger import logging
from . models import Posts, Response, CommentsResponse, BlogGallery, Subscription
from django.conf import settings

from django.utils import timezone
from datetime import datetime





def user_registeration(request):
    if request.method == "POST":
        logging.info("User Registration process started")
        form = CustomUserForm(request.POST)
        logging.info("Grabbed all the details from form.")

        if form.is_valid():
            logging.info("All details are valid. creating user...")
            
            try:
                user = form.save()
                messages.success(request, "User Registered Successfully")
                message = "User Registerd Successfully"
                # if user valid then login code, uncomment below code
                #login(request,user)

            except Exception as e:
                message = "Error occured During registration follow the details"
                logging.info(e)
            finally:
                return render(request,"blogs/signup.html", {"register_form":form, "message":message})
        else:
            logging.info(f"details are not valid{form.add_error}")
            message = "Error occured During registration follow the details"
       
        messages.error(request, "Problem Occurred During registration")
    form = CustomUserForm()
    return render(request,"blogs/signup.html", {"register_form":form, "message":""})

def login_request(request):
    if request.user.is_authenticated:
        content = load_dashboard_content(request)
        sub_status = Subscription.objects.get(user = request.user)
        return render(request,"blogs/dashboard.html",{"contents":content,"sub_status": sub_status})
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username= username, password=password)
        if user is not None:
            login(request,user)
            
            if ensure_user_in_sub_model(request):
                logging.info("checking user in subs model ")
                sub_status = Subscription.objects.get(user = request.user)
                return render(request,"blogs/dashboard.html",{"contents":content,"sub_status": sub_status})
            else:
                return HttpResponse("problem occured in registering user in sub model")
    form = AuthenticationForm()
    
    return render(request, "blogs/login.html",{"login_form": form})

def logout_request(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                auth.logout(request)
                message = "loggedout successfully"
            except Exception as e:
                message = "error occured during logout"
                logging.info(e)
            finally:
                return render(request, "blogs/login.html", {"message":message})
            
def load_dashboard_content(request):
    if request.user.is_authenticated:
        content = Posts.objects.all().order_by('-pub_date')
        print(content)
        return content
    
def create_blog(request):
    logging.info("Creating blog")
    if request.method == "POST":

        if request.user.is_authenticated:
            print("all okay")
            author = request.user
            title = request.POST['title']
            content = request.POST['content']
            image = request.FILES['image']
            new_content = Posts(author_name = author, title = title,content = content, image = image)
            new_content.save()
            print(author, title, content)
            content = load_dashboard_content(request)
            return render(request,"blogs/dashboard.html",{"contents":content})
    return render(request,"blogs/create_blog.html")

def read_blog(request, post_id):
    if request.user.is_authenticated:
        post = Posts.objects.get(pk=post_id)
        if not blog_read_access(request,post_id):
            sub_instance = Subscription.objects.get(user=request.user)
            one=sub_instance.accessed_blog_one
            return HttpResponse(f'you have reached your daily limit of access. come again or  read articles open for you \
                                <a href ="http://127.0.0.1:8000/blogs/{sub_instance.accessed_blog_one}">one</a> <a href ="http://127.0.0.1:8000/blogs/{sub_instance.accessed_blog_two}">two</a>. or purchase the subscription for unlimited access ')
        content = post
        likes_total = load_likes(request,post_id)
        likes_total = likes_total.count()
        comments = load_comment(request, post_id)
        like_button_status = get_like_status(request, post_id)
        print("Total likes",likes_total)
        print(content.pk)
        gallery = fetch_gallery(request, post_id)
        logging.info("updating daily read count")
        upate_daily_read_count(request,post_id)
        return render(request, "blogs/blog.html",{"content":content,"likes":likes_total, "comments": comments, "like_status": like_button_status,"gallery":gallery})
    
def get_like_status(request, post_id):
    instatance = Response.objects.filter(post_id = post_id, username = request.user.username,nested = False)
    if instatance.count():
        current_post_like_instance = Response.objects.filter(post_id = post_id, username = request.user.username, nested = False, like=True)
        if current_post_like_instance:
            if current_post_like_instance[0].like == True:
                return True
        else:
            return False
        
    return False

def register_likes(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            logging.info("user is logged")            
            username = request.user.username
            post_id = request.POST['post_id']
            logging.info(f"request is made to alter like for post id {post_id} by {username}")
            print(post_id)
            
            response_instance =  Response.objects.filter(post_id = post_id, username=username, nested = False, comment_flag = False)

            logging.info(response_instance)

            if response_instance.count():
                logging.info(f"Previous request found in db, altering")
                response_instance_object = Response.objects.get(post_id = post_id, username=username,nested = False, comment_flag = False)
                print(username)
                if response_instance_object.like == False:
                    response_instance_object.like = True
                else:
                    response_instance_object.like = False
                response_instance_object.save()
                    
            else:
                logging.info("Registering response for the first time")
                response_instance = Response(post_id = post_id, username = request.user.username, like = True, nested=False)
                response_instance.save()
                logging.info("response saved")
            # content = load_dashboard_content(request)
            # return render(request,"blogs/dashboard.html",{"contents":content})
            return read_blog(request,post_id)
        
    content = load_dashboard_content(request)
    return render(request,"blogs/dashboard.html",{"contents":content})
    

def load_likes(request, post_id):
    likes = Response.objects.filter(post_id = post_id, like = True, nested = False)
    print("likes : ",likes)
    return likes
def load_comment(request, post_id):
    comments = Response.objects.filter(post_id = post_id, nested= False).order_by("-first_response_date")
    print("comment : ",comments)
    comment_return = dict()
    for count,comment in enumerate(comments):
        temp_0 = list()
        comment_return[count] = dict()
        temp_0.append(comment)
        temp_0.append(load_comment_reaction(request,comment.pk))
        comment_return[count]["comment"] = temp_0
        replies = load_replies(request, post_id, comment.pk)
        comment_return[count]["replies"] = list()
        for reply in replies:
            temp = list()
            temp.append(reply)
            temp.append(load_comment_reaction(request,reply.pk))
            comment_return[count]["replies"].append(temp)
    print(comment_return)
    return comment_return

def load_comment_reaction(request,comment_id):
    likes_instance = CommentsResponse.objects.filter(response = comment_id, reaction = "Like")
    Dislikes_instance = CommentsResponse.objects.filter(response = comment_id, reaction = "Dislike")
    return {"comment_id": comment_id,"Likes": likes_instance.count(), "Dislikes": Dislikes_instance.count()}

def load_replies(request, post_id, comment_id):
    replies = Response.objects.filter(post_id = post_id,nested_response_id=comment_id, nested= True).order_by("-first_response_date")
    print("comment : ",replies)
    return replies


def register_comment(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            logging.info("user is logged")            
            username = request.user.username
            post_id = request.POST['post_id']
            comment = request.POST['comment']
            logging.info(f"request is made to make comment for  post id {post_id} by {username}")
            print(post_id)
            
            response_instance =  Response.objects.filter(post_id = post_id, username=username)

            logging.info(response_instance)

            #if response_instance.count():
            if False:
                logging.info(f"Previous request found in db, altering")
                response_instance_object = Response.objects.get(post_id = post_id, username=username)
                response_instance_object.comment = comment
                response_instance_object.save()
                    
            else:
                logging.info("Registering response for the first time")
                response_instance = Response(post_id = post_id, username = request.user.username, comment = comment,comment_flag = True)
                response_instance.save()
                logging.info("response saved")
            # content = load_dashboard_content(request)
            # return render(request,"blogs/dashboard.html",{"contents":content})
            return read_blog(request,post_id)

    content = load_dashboard_content(request)
    return render(request,"blogs/dashboard.html",{"contents":content})


def register_comment_reply(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            logging.info("user is logged")            
            username = request.user.username
            post_id = request.POST['post_id']
            comment_id = request.POST['comment_id']
            comment = request.POST['comment']
            logging.info(f"request is made to make reply on comment id {comment_id} by {username}")
            print(comment_id)
            
            # response_instance =  Response.objects.filter(pk = comment_id, username=username)

            # logging.info(response_instance)

            #if response_instance.count():
            if False:
                logging.info(f"Previous request found in db, altering")
                response_instance_object = Response.objects.get(post_id = post_id, username=username)
                response_instance_object.comment = comment
                response_instance_object.save()
                    
            else:
                logging.info("Registering response for the first time")
                response_instance = Response(post_id=post_id,username = request.user.username, comment = comment,comment_flag = True, nested = True, nested_response_id = comment_id)
                response_instance.save()
                logging.info("response saved")
            # content = load_dashboard_content(request)
            # return render(request,"blogs/dashboard.html",{"contents":content})
            return read_blog(request,post_id)

    content = load_dashboard_content(request)
    return render(request,"blogs/dashboard.html",{"contents":content})
            



def register_comment_reaction(request):
    

    if request.user.is_authenticated:
        user  =  request.user
        response_id = request.POST.get("comment_id")  # response_pk
        post_id = request.POST.get("post_id")
        reaction = request.POST["choice"]
        print("post id",post_id, type(response_id), user, reaction)
        
        response_exist = CommentsResponse.objects.filter(response = response_id, user_name = user)
        print(post_id, user, response_id, reaction)

        if response_exist.count():
            response_instance = CommentsResponse.objects.get(response = response_id, user_name = user)
            response_instance.reaction = reaction
            response_instance.save()
                
        else:
            response_instance = CommentsResponse(user_name = user , response = Response.objects.get(pk=response_id), reaction = reaction)
            response_instance.save()
            logging.info("comment reaction registerd successfully")
        return read_blog(request, post_id)

    return read_blog(request, post_id)

def load_reaction_status(request,comment_id, user):
    pass


def upload_to_gallery(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            post_id = int(request.POST.get("post_id"))
            images = request.FILES.getlist('images')
            for image in images:
                print(post_id, type(post_id), image)
                BlogGallery.objects.create(posts = Posts.objects.get(pk = post_id), images = image)
    return read_blog(request, post_id)

def fetch_gallery(request, post_id):
    gallery_instance = BlogGallery.objects.filter(posts=post_id).order_by("-upload_date")
    return gallery_instance
def open_editor(request):
    if request.method =="POST":
        post_id = request.POST['post_id']



def post_editor(request):
    if request.method == "POST":
        post_id = request.POST['post_id']
        if request.user.is_authenticated:
            post_instance = Posts.objects.get(pk=post_id)
            if str(request.user.username) == str(post_instance.author_name):
                title = request.POST['title']
                content = request.POST['content']
                print(title,content)
                image = request.FILES.get('image')
                print(image, type(image))
                post_instance.title = title
                post_instance.content = content
                if image:
                    post_instance.image = image
                post_instance.save()
                return read_blog(request, post_id)
            else:
                print(type(post_instance.author_name))
                return HttpResponse(f'You dont have required privleges to edit this blog, only author have the right to make changes.\
                                    <a href ="{post_id}">click  here</a> to go back ')
        return HttpResponse("Authentication is required to access post editor")
    elif request.method == "GET":
        post_id = request.GET.get('post_id', None)    
        post_instance = Posts.objects.get(pk=post_id)
        return render(request,"blogs/editor.html", {"form": post_instance})
    

def ensure_user_in_sub_model(request)->bool:
    if request.user.is_authenticated:
        sub_instance = Subscription.objects.filter(user = request.user)
        if sub_instance.count():
            current_datetime = timezone.now().date()
            sub_instance = Subscription.objects.get(user= request.user)
            if sub_instance.last_logged_in<current_datetime:
                sub_instance.daily_read_count = 0
                sub_instance.accessed_blog_one = None
                sub_instance.accessed_blog_two = None
            return True
        else:
            sub_instance = Subscription(user = request.user)
            sub_instance.save()
            return True
    return False

def upate_daily_read_count(request, post_id):

    try:
        sub_instance = Subscription.objects.get(user = request.user)
        if sub_instance.accessed_blog_one is None:
            sub_instance.accessed_blog_one = post_id
        elif sub_instance.accessed_blog_one != post_id and sub_instance.accessed_blog_two is None:
            sub_instance.accessed_blog_two = post_id 

        logging.info(f"{sub_instance.daily_read_count}")
        sub_instance.daily_read_count += 1
        logging.info(f"{sub_instance.daily_read_count}")
        sub_instance.save()
    except Exception as e:
        logging.info(e)
    else:
        logging.info(f"returning")
        return None
    
def blog_read_access(request,post_id)->bool:
    sub_instance = Subscription.objects.get(user=request.user)
    if sub_instance.subscription_status == False:
        if sub_instance.daily_read_count<=2:
            return True
        else:
            if sub_instance.accessed_blog_one == post_id or sub_instance.accessed_blog_two == post_id:
                return True
            else:
                False
    elif sub_instance.subscription_status == True:
        return True
    
    else:
        return False
    

def subscribe(request):
    if request.user.is_authenticated:
        sub_instance = Subscription.objects.get(user = request.user)
        if sub_instance.subscription_status:
            sub_instance.subscription_status = False
            sub_instance.save()
        else:
            sub_instance.subscription_status = True
            sub_instance.save()

    return login_request(request)
            

