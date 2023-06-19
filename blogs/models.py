from django.db import models

class Posts(models.Model):
    post_id = models.AutoField
    title = models.CharField(max_length= 50)
    author_name = models.CharField(max_length=20)
    content = models.CharField(max_length=500)
    image = models.ImageField(upload_to="blogs/images", default = "")
    #likes_count = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    last_edit_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Response(models.Model):
    post_id = models.CharField(max_length=20)
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
            
        
        return self.username + "-" + self.post_id + "-" +  l_status + "  Nested :"+ str(self.nested ) + "  | Comment :   "+ self.comment