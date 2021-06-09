from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listings, Bidding, Comments, WishList, CloseListing, Titles

CATEGORIES = ["Sports", "Entertainment", "Home", "Kids", "Toys", "Gaming", "Education", "Beauty and Wellness"]


def index(request):
    rows = Listings.objects.all()
    
    

    return render(request, "auctions/index.html", {
        "rows":rows
    })

    temp2 = Listings.objects.exclude(title=CloseListing.objects.all()).all()
    return HttpResponse(temp2)

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="login")
def create_listing(request):
    if request.method == "POST":
        results = request.POST
        # check if neccessary fields are all filled in
        i = 0
        if len(results["title"]) == 0 or len(results["description"]) == 0 or len(results["starting_bid"]) == 0:
            return render(request, "auctions/create_listing.html", {
                "categories": CATEGORIES,
                "message": "Must provide title, description and starting bid"
            })
        else:
            title = results["title"]
            description = results["description"]
            starting_bid = results["starting_bid"]

            # optional inputs
            if len(results["image_link"]) != 0:
                image_link = results["image_link"]
            else:
                image_link = None
            if len(results["category"]) != 0:
                category = results["category"]
            else:
                category = None

        # username
        username = request.user
        
        # create new title in titles table
        temp = Titles.objects.create(title=title)
        temp.save()

        row = Listings.objects.create(seller_id=username, title=temp, description=description, starting_bid=starting_bid, image_link=image_link, category=category)
        row.save()
        return HttpResponseRedirect(reverse("index"))
        
    else:
        return render(request, "auctions/create_listing.html", {
            "categories": CATEGORIES
        })


def listing(request, listing_name, title_id):
    title_name = Titles.objects.get(title=listing_name, id=title_id)

    listing_row = Listings.objects.get(title=title_name)

    # wishlist
    if request.user.username != "" :
        if WishList.objects.filter(user_id=request.user, wishlist_title=title_name).count() == 1:
            wishlist = WishList.objects.get(user_id=request.user, wishlist_title=title_name)
        else:
            wishlist = False
    else:
        wishlist = False

    # existing bids for this listing
    if Bidding.objects.filter(bids_title=title_name).count() != 0:
        bids = list(Bidding.objects.filter(bids_title=title_name).all())
    else:
        bids = False

    # if listing is closed
    if CloseListing.objects.filter(title=title_name).count() == 1:
        closed = CloseListing.objects.get(title=title_name)
    else:
        closed = False
    
    # Comments
    if Comments.objects.filter(comments_title=title_name).count() != 0:
        comments = Comments.objects.filter(comments_title=title_name).all()
    else:
        comments = False

    return render(request, "auctions/listing.html", {
        "listing": listing_row,
        "wishlist": wishlist,
        "bids": bids,
        "closed": closed,
        "comments": comments
    })

@login_required(login_url="login")
def wishlist(request):
    if request.method == "POST":
        title = request.POST["title"]
        title_id = request.POST["title_id"]
        title_name = Titles.objects.get(title=title, id=title_id)

        # add wishlist
        if WishList.objects.filter(user_id=request.user, wishlist_title=title_name).count() == 0:
            temp = WishList.objects.create(user_id=request.user, wishlist_title=title_name)
            temp.save()
        # remove wishlist
        else:
            temp = WishList.objects.get(user_id=request.user, wishlist_title=title_name)
            temp.delete()
        return HttpResponseRedirect(reverse("wishlist"))
    else:
        # get info from db
        wish_rows = list(WishList.objects.filter(user_id=request.user).all())
        wish_titles = []
        # get name of wish list titles
        for row in wish_rows:
            wish_titles.append(row.wishlist_title)
        
        # query data from Listings
        rows = []
        for row in wish_titles:
            rows.append(Listings.objects.get(title=row))

        return render(request, "auctions/wishlist.html", {
            "rows": rows
        })

@login_required(login_url="login")
def bid(request):
    if request.method == "POST":
        money = float(request.POST["bid"])
        title = request.POST["title"]
        title_id = request.POST["title_id"]
        title_name = Titles.objects.get(title=title, id=title_id)
        
        # see if there are any existing bids
        rows = list(Bidding.objects.filter(bids_title=title_name).all())

        # store existing bids in a list
        bids = []
        for row in rows:
            bids.append(row.bid)
        
        # check if user bid is higher than existing ones and minimum bid
        min_bid = Listings.objects.get(title=title_name).starting_bid

        for bid in bids:
            if money <= bid:
                return render(request, "auctions/error.html", {
                    "message": "You must place a bid greater than existing bids!"
                })
        if money < min_bid:
            return render(request, "auctions/error.html", {
                    "message": "You must place a bid greater than the starting bid!"
                })
        # create bid in db
        temp = Bidding.objects.create(buyer_id=request.user, bids_title=title_name, bid=money)
        temp.save()
        return HttpResponseRedirect(reverse("listing", kwargs={"listing_name": title, "title_id":title_id}))

@login_required(login_url="login")
def remove_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        title_id = request.POST["title_id"]
        title_name = Titles.objects.get(title=title, id=title_id)

        # highest bidder wins
        winner = Bidding.objects.filter(bids_title=title_name).order_by("-bid")[0]

        # create row in db
        temp = CloseListing.objects.create(title=title_name, winner=winner.buyer_id, bid=winner.bid)
        temp.save()

        # update listings table for closed column to true
        temp = Listings.objects.get(title=title_name).update(closed=True)

        # delete bidding rows
        temp = Bidding.objects.filter(bids_title=title_name).all()
        temp.delete()

        return HttpResponseRedirect(reverse("listing", kwargs={"listing_name": title, "title_id":title_id}))

@login_required(login_url="login")
def closedlisting(request):
    if CloseListing.objects.filter(winner=request.user).count() != 0:
        rows = CloseListing.objects.filter(winner=request.user).all()
        list_all = []
        if rows.count() != 0:
            for row in rows:
                title_name = row.title
                
                bid = row.bid

                listing_row = Listings.objects.get(title=title_name)

                list_all.append({"listing_row":listing_row, "bid":bid})
                
            
            return render(request, "auctions/closedlisting.html", {
                "listing_rows": list_all
            })
    else:
        return render(request, "auctions/closedlisting.html")

def category(request, type):
    if type == "all":
        return render(request, "auctions/category.html", {
            "categories": CATEGORIES
        })
    else:
        rows = Listings.objects.filter(category=type, closed=False)
        
        return render(request, "auctions/type.html", {
            "type": type,
            "rows": rows
        })

@login_required(login_url="login")
def comments(request):
    if request.method == "POST":
        comment = request.POST["comment"]
        if len(comment) > 64:
            return render(request, "auctions/error.html", {
                "message": "Length of Comment must not exceed 64 characters!"
            })
        title_id = request.POST["title_id"]
        title_name = Titles.objects.get(id=title_id)
        temp = Comments.objects.create(user_id=request.user, comments_title=title_name , comment=comment)
        temp.save()

        return HttpResponseRedirect(reverse("listing", kwargs={"listing_name": title_name, "title_id":title_id}))
    else:
        pass

def deletecomment(request):
    if request.method == "POST":
        title_id = request.POST["title_id"]
        title_name = Titles.objects.get(id=title_id)
        comment_id = request.POST["comment_id"]
        temp = Comments.objects.get(comments_title=title_name, user_id=request.user, id=comment_id)
        temp.delete()

        return HttpResponseRedirect(reverse("listing", kwargs={"listing_name": title_name, "title_id":title_id}))