
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("new", views.new, name="new"),
    path("post/<int:post_id>", views.post, name="post"),
    path("posts", views.posts, name="posts"),
    path("posts/<int:user_id>", views.posts, name="posts")
]
