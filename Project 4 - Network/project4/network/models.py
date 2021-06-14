from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank= False)
    time = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(blank= False, default= 0)

    def __str__(self):
        return f"{self.id}: {self.user}"

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.IntegerField(default= 0)
    followers = models.IntegerField(default= 0)

    def __str__(self):
        return f"{self.user}"

class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    idol = models.ForeignKey(User, on_delete=models.CASCADE, related_name="idol")
    following = models.BooleanField(blank=False)

    def __str__(self):
        return f"{self.user} follows {self.idol} ({self.following})"
