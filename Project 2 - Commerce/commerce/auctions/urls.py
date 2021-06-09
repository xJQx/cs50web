from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("bid", views.bid, name="bid"),
    path("remove_listing", views.remove_listing, name="remove_listing"),
    path("closedlisting", views.closedlisting, name="closedlisting"),
    path("category/<str:type>", views.category, name="category"),
    path("comments", views.comments, name="comments"),
    path("delete-comment", views.deletecomment, name="deletecomment"),
    path("<str:listing_name>&<str:title_id>", views.listing, name="listing")
]
