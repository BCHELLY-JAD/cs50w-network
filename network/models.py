from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False, blank=True)
    
    def count_followers(self):
        return self.followers.count()

    def count_following(self): 
        return self.following.count()

    def serialize(self):
        return { 
            "followers": self.followers,
            "count_followers": user.count_followers(),
            "count_following": user.count_following()
        }


class Post(models.Model): 
    post_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="person")
    post_content = models.CharField(blank=False, max_length=160)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    likes = models.ManyToManyField(User)
    
    def likes_count(self): 
        return self.likes.count()

    def serialize(self): 
        return{ 
        "id": self.id,
        "post_owner": self.post_owner,
        "post_content": self.post_content,
        "timestamp": self.timestamp,
        "likes": self.liked
        }








