from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<int:user_id>", views.profile, name="profile"),
    path("Following", views.following_page, name="following"),
    path("toggle/<int:user_id>", views.follow, name="follow"),
    path("like/<int:post_id>", views.like, name="like"),
    path("save/<int:post_id>", views.edit, name="edit")
]
