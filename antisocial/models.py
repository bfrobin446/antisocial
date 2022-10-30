import uuid

from django.conf import settings
from django.db import models


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    save_time = models.DateTimeField(auto_now_add=True)
    supersedes = models.OneToOneField(
        to="Post",
        on_delete=models.PROTECT,
        related_name="updated",
        null=True,
        blank=True,
    )
    body = models.TextField()
    tags = models.ManyToManyField("Tag", related_name="posts")


class Tag(models.Model):
    id = models.SlugField(primary_key=True)
    display_name = models.CharField(max_length=64)
    description = models.TextField()
