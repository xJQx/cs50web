from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("editpage/<str:title>", views.editpage, name="editpage"),
    path("random/", views.random, name="random"),
    path("<str:title>/", views.title, name="title")
]
