from django.urls import path
from . import views

app_name = "blogs"
urlpatterns = [
    path("user_registeration/", views.user_registeration, name = "user_registeration"),
    path("login_request", views.login_request, name="login_request"),
    path("logout_request", views.logout_request, name="logout_request"),
    path("create_blog", views.create_blog, name="create_blog"),
    path("read_blog", views.read_blog, name="read_blog"),
    path("<int:post_id>/", views.read_blog, name="read_blog"),
    path("register_likes", views.register_likes, name="register_likes"),
    path("register_comment", views.register_comment, name="register_comment"),
    path("register_comment_reply", views.register_comment_reply, name="register_comment_reply"),
    path("register_comment_reaction", views.register_comment_reaction, name="register_comment_reaction"),
    path("upload_to_gallery", views.upload_to_gallery, name="upload_to_gallery"),
    path("post_editor", views.post_editor, name="post_editor"),
    path("open_post_editor/<int:post_id>/", views.post_editor, name="post_editor"),
]