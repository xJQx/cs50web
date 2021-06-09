from django.contrib.auth.models import AbstractUser
from django.db import models

# MAX_LENGTH for input fields
LENGTH = 64

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"
    pass

class Titles(models.Model):
    title = models.CharField(max_length=LENGTH, blank=False, null=True)

    def __str__(self):
        return f"{self.title}"

class Listings(models.Model):
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)
    description = models.CharField(max_length=LENGTH, blank=False, null=True)
    starting_bid = models.FloatField(default=0)
    image_link = models.CharField(max_length=256, blank=True, null=True)
    category = models.CharField(max_length=256, blank=True, null=True)
    closed = models.BooleanField(blank=False, default=False)

    def __str__(self):
        return f"{self.title}"

class Comments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    comments_title = models.ForeignKey(Titles, on_delete=models.CASCADE)
    comment = models.CharField(max_length=LENGTH, blank=False, null=True)

    def __str__(self):
        return f"{self.user_id}"

class WishList(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    wishlist_title = models.ForeignKey(Titles, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id}: {self.wishlist_title}"

class Bidding(models.Model):
    buyer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")
    bids_title = models.ForeignKey(Titles, on_delete=models.CASCADE)
    bid = models.FloatField(blank=False, null=True)

    def __str__(self):
        return f"{self.buyer_id}: {self.bids_title}({self.bid})"

class CloseListing(models.Model):
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)
    winner = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.FloatField(blank=False, null=True)

    def __str__(self):
        return f"{self.title}"
