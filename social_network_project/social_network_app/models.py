from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
	last_request = models.DateTimeField(null=True, blank=True, default=None)


class SimplePost(models.Model):
	author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='own_posts')
	title = models.CharField(max_length=255, null=True, blank=True)
	content = models.TextField(null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
	author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='own_likes')
	post = models.ForeignKey(SimplePost, on_delete=models.CASCADE, null=True, blank=True, related_name='post_likes')
	created = models.DateField(auto_now_add=True, blank=True, null=True)

	class Meta:
		unique_together = ['author', 'post']
