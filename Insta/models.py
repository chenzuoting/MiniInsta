from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from imagekit.models import ProcessedImageField

# Create your models here.

class InstaUser (AbstractUser):
    profile_pic = ProcessedImageField(
        upload_to='static/images/profiles',
        format='JPEG',
        options={'quality': 100},
        null=True,
        blank=True,
        )

    def get_absolute_url(self): #called when new post saved
        return reverse("user_profile", args=[str(self.id)]) #get url based on name

    def get_connections(self):
        return UserConnection.objects.filter(creator=self)
    
    def get_followers(self):
        return UserConnection.objects.filter(following=self)

    def is_followed_by(self, user):
        followers = UserConnection.objects.filter(following=self)
        return followers.filter(creator=user).exists()

class Post (models.Model):
    author = models.ForeignKey(
        InstaUser,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.TextField(blank=True, null=True)
    image = ProcessedImageField(
        upload_to='static/images/posts',
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True,
    )

    def get_absolute_url(self): #called when new post saved
        return reverse("post_detail", args=[str(self.id)]) #get url based on name

    def get_like_count(self):
        return self.likes.count()

    def get_comment_count(self):
        return self.comments.count()

class UserConnection(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friendship_creator_set"
    )
    following = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friend_set"
    )

    def __str__(self):
        return self.creator.username + ' follows ' + self.following.username

class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        #related_name: define here so that its foreign key object, post, can visit it  with this name 
        #and get all the connections with current post
        related_name='likes'
    )
    user = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    class Meta:
        # Use this in a relation model, determine if we need some unique info 
        # Combination post and user should be unique
        unique_together = ("post", "user")

    # Display as string
    def __str__(self):
        return 'Like: ' + self.user.username + ' likes ' + self.post.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',)
    user = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    posted_on = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.comment