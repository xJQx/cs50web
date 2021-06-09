from django.contrib import admin

from .models import User, Listings, Bidding, Comments, WishList, CloseListing, Titles

# Register your models here.
admin.site.register(User)
admin.site.register(Titles)
admin.site.register(Listings)
admin.site.register(Bidding)
admin.site.register(Comments)
admin.site.register(WishList)
admin.site.register(CloseListing)