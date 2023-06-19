from django.shortcuts import render
from . forms import CustomUserForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm
import sys
import os
from . logger import logging
from . models import Posts, Response


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
        return render(request,"blogs/dashboard.html",{"contents":content})
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username= username, password=password)
        if user is not None:
            login(request,user)
            content = load_dashboard_content(request)
            return render(request,"blogs/dashboard.html",{"contents":content})
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
            author = request.user.username
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
        content = post
        likes_total = load_likes(request,post_id)
        likes_total = likes_total.count()
        comments = load_comment(request, post_id)
        like_button_status = get_like_status(request, post_id)
        print("Total likes",likes_total)
        print(content.pk)
        return render(request, "blogs/blog.html",{"content":content,"likes":likes_total, "comments": comments, "like_status": like_button_status})
    
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
        comment_return[count] = dict()
        comment_return[count]["comment"] = comment
        replies = load_replies(request, post_id, comment.pk)
        comment_return[count]["replies"] = list()
        for reply in replies:
            comment_return[count]["replies"].append(reply)
    print(comment_return)
    return comment_return

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
            



