from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

from .models import User, Posts, Follow, Following


def index(request):
    # new post
    if request.method == "POST":
        # get content and change if there is any content
        content = request.POST["content"]
        if len(content) == 0:
            # query post
            posts = Posts.objects.filter().all()
            posts = posts.order_by('time').reverse()

            return render(request, "network/index.html", {
                "message": "Must write content before posting!",
                "posts": posts
            })
        else:
            # create post
            temp = Posts.objects.create(user=request.user, content=content, likes=0)
            temp.save()

            return HttpResponseRedirect(reverse(index))
    else:
        # query post
        posts = Posts.objects.filter().all()
        posts = posts.order_by('time').reverse()

        # pages
        page_len = 1
        count = 0
        for i in posts:
            # for every 10 posts
            if count != 0:
                if count % 10 == 0:
                    page_len += 1
            count += 1

        p = Paginator(posts, 10)
        
        # list of pages list
        temp_list = []
        for i in range(page_len):
            temp_page = p.get_page(i + 1)
            temp_list.append(temp_page.object_list)
        
        posts = temp_list[0]
        page_num = 1
        
        return render(request, "network/index.html", {
            "posts": posts,
            "page_num": page_num,
            "page_len": page_len
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url="login")
def profile(request, user):
    user = User.objects.get(username=user)

    posts = Posts.objects.filter(user=user).all()
    posts = posts.order_by('time').reverse()

    if len(Follow.objects.filter(user=user).all()) == 0:
        temp = Follow.objects.create(user=user)
        temp.save()

    follows = Follow.objects.filter(user=user).all()

    if request.user != user:
        if len(Following.objects.filter(user=request.user, idol=user).all()) == 0:
            temp2 = Following.objects.create(user=request.user, idol=user, following=False)
            temp2.save()
    
    following = Following.objects.filter(user=request.user, idol=user).all()

    # pages
    page_len = 1
    count = 0
    for i in posts:
        # for every 10 posts
        if count != 0:
            if count % 10 == 0:
                page_len += 1

        count += 1

    p = Paginator(posts, 10)
    
    # list of pages list
    temp_list = []
    for i in range(page_len):
        temp_page = p.get_page(i + 1)
        temp_list.append(temp_page.object_list)
    
    posts = temp_list[0]
    page_num = 1

    return render(request, "network/profile.html", {
        "posts": posts,
        "follows": follows,
        "following": following,
        "page_num": page_num,
        "page_len": page_len
    })

def follow(request):
    if request.method == "POST":
        follow_type = request.POST["follow_type"]
        if follow_type == "follow":
            follow_type = True
        elif follow_type == "unfollow":
            follow_type = False
        
        idol = request.POST["idol"]
        idol = User.objects.get(username=idol)

        # update follows row for user and idol
        if len(Follow.objects.filter(user=request.user).all()) == 0:
            Follow.objects.create(user=request.user)
        temp = Follow.objects.get(user=request.user)
        temp2 = Follow.objects.get(user=idol)

        if follow_type == True:
            temp.following += 1
            temp.save()

            temp2.followers += 1
            temp2.save()
        else:
            temp.following -= 1
            temp.save()

            temp2.followers -= 1
            temp2.save()

        # update following row for user
        temp3 = Following.objects.get(user=request.user, idol=idol)
        temp3.following = follow_type
        temp3.save()

        return HttpResponseRedirect(reverse(profile, kwargs={"user": idol}))

def following(request):
    # store a list of idols
    idols = []
    user = User.objects.get(username=request.user)
    temp = Following.objects.filter(user=user, following=True)
    for idol in temp:
        idols.append(idol.idol)
    
    # query posts
    posts = Posts.objects.filter(user__in=idols).all()
    posts = posts.order_by('time').reverse()

    # pages
    page_len = 1
    count = 0
    for i in posts:
        # for every 10 posts
        if count != 0:
            if count % 10 == 0:
                page_len += 1
        count += 1

    p = Paginator(posts, 10)
    
    # list of pages list
    temp_list = []
    for i in range(page_len):
        temp_page = p.get_page(i + 1)
        temp_list.append(temp_page.object_list)
    
    posts = temp_list[0]
    page_num = 1
    
    return render(request, "network/following.html", {
            "posts": posts,
            "page_num": page_num,
            "page_len": page_len
        })

def page(request, page_num):
    # query post
    posts = Posts.objects.filter().all()
    posts = posts.order_by('time').reverse()

    # pages
    page_len = 1
    count = 0
    for i in posts:
        # for every 10 posts
        if count != 0:
            if count % 10 == 0:
                page_len += 1
        count += 1

    p = Paginator(posts, 10)
    
    # list of pages list
    temp_list = []
    for i in range(page_len):
        temp_page = p.get_page(i + 1)
        temp_list.append(temp_page.object_list)
    
    posts = temp_list[page_num - 1]

    return render(request, "network/index.html", {
        "posts": posts,
        "page_num": page_num,
        "page_len": page_len
    })

def fpage(request, page_num):
    # store a list of idols
    idols = []
    user = User.objects.get(username=request.user)
    temp = Following.objects.filter(user=user, following=True)
    for idol in temp:
        idols.append(idol.idol)
    
    # query posts
    posts = Posts.objects.filter(user__in=idols).all()
    posts = posts.order_by('time').reverse()

    # pages
    page_len = 1
    count = 0
    for i in posts:
        # for every 10 posts
        if count != 0:
            if count % 10 == 0:
                page_len += 1
        count += 1

    p = Paginator(posts, 10)
    
    # list of pages list
    temp_list = []
    for i in range(page_len):
        temp_page = p.get_page(i + 1)
        temp_list.append(temp_page.object_list)
    
    posts = temp_list[page_num - 1]

    return render(request, "network/following.html", {
        "posts": posts,
        "page_num": page_num,
        "page_len": page_len
    })

def ppage(request, user,  page_num):
    user = User.objects.get(username=user)
    page_num = int(page_num)
    
    posts = Posts.objects.filter(user=user).all()
    posts = posts.order_by('time').reverse()

    if len(Follow.objects.filter(user=user).all()) == 0:
        temp = Follow.objects.create(user=user)
        temp.save()

    follows = Follow.objects.filter(user=user).all()

    if request.user != user:
        if len(Following.objects.filter(user=request.user, idol=user).all()) == 0:
            temp2 = Following.objects.create(user=request.user, idol=user, following=False)
            temp2.save()
    
    following = Following.objects.filter(user=request.user, idol=user).all()

    # pages
    page_len = 1
    count = 0
    for i in posts:
        # for every 10 posts
        if count != 0:
            if count % 10 == 0:
                page_len += 1
        count += 1

    p = Paginator(posts, 10)
    
    # list of pages list
    temp_list = []
    for i in range(page_len):
        temp_page = p.get_page(i + 1)
        temp_list.append(temp_page.object_list)
    
    posts = temp_list[page_num - 1]

    return render(request, "network/profile.html", {
        "posts": posts,
        "follows": follows,
        "following": following,
        "page_num": page_num,
        "page_len": page_len
    })

@csrf_exempt
def editpost(request, post_id):
    if request.method == "PUT":
        temp = Posts.objects.get(id= post_id)
        if request.user != temp.user:
            return HttpResponseRedirect(reverse(index))

        data = json.loads(request.body)
        if data.get("content") is not None:
            temp.content = data["content"]
        temp.save()
        return HttpResponse(status=204)
    else:
        return HttpResponseRedirect(reverse(index))

@csrf_exempt
def likepost(request, post_id):
    if request.method == "PUT":
        temp = Posts.objects.get(id= post_id)

        data = json.loads(request.body)
        if data.get("likes") is not None:
            total_likes = int(temp.likes) + data["likes"]
            temp.likes = total_likes
        temp.save()

        return HttpResponse(status=204)
    else:
        return HttpResponseRedirect(reverse(index))