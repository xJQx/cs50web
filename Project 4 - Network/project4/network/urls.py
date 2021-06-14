
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("follow", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("editpost/<int:post_id>", views.editpost, name="editpost"),
    path("likepost/<int:post_id>", views.likepost, name="likepost"),
    path("<int:page_num>", views.page, name="page"),
    path("following/<int:page_num>", views.fpage, name="fpage"),
    path("<str:user>/<str:page_num>", views.ppage, name="ppage"),
    path("<str:user>", views.profile, name="profile")
]
