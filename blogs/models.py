from django.db import models
from django.contrib.auth.models import User

class Posts(models.Model):
    post_id = models.AutoField
    title = models.CharField(max_length= 50)
    author_name = models.ForeignKey(User, on_delete = models.CASCADE) #models.CharField(max_length=20)
    content = models.CharField(max_length=500)
    image = models.ImageField(upload_to="blogs/images", default = "")
    #likes_count = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    last_edit_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + str(self.pk)

class Response(models.Model):
    post_id = models.CharField(max_length=20) #models.ForeignKey(Posts, on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    like = models.BooleanField(default=False)
    comment = models.CharField(max_length=100, blank=True)
    first_response_date = models.DateTimeField(auto_now_add=True)
    last_response_edit_date = models.DateTimeField(auto_now=True)
    nested = models.BooleanField(default=False, blank=True)
    nested_response_id = models.CharField(default= "",blank=True, max_length=4)
    comment_flag = models.BooleanField(default=False)


    def __str__(self):
        l_status = str(self.like)
        if self.like:
            l_status = "like response"
            abc = self.username + "-" + self.post_id + "-" +  l_status + "  Nested :"+ str(self.nested ) + "  | Comment :   "+ self.comment
            return abc
        return str(self.post_id) +"-"+ str(self.username)+"-"+ str(self.pk)
    
class CommentsResponse(models.Model):
    response = models.ForeignKey(Response,on_delete=models.CASCADE)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.CharField(default="", max_length=8)


    def __str__(self) -> str:
        return str(self.user_name) + str(self.response)

 
class BlogGallery(models.Model):
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE, default="")
    images = models.ImageField(upload_to="blogs/gallery")
    upload_date = models.DateField(auto_now_add=True)