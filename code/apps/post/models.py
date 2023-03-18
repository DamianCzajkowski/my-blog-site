from utlis.util_models import TimeStampModel

from apps.user.models import User
from django.db import models


class Post(TimeStampModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to="static/uploads/")
    banner_image = models.ImageField(upload_to="static/uploads/", null=True, blank=True)
    thumb_image = models.ImageField(upload_to="static/uploads/", null=True, blank=True)
    is_public = models.BooleanField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag")
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user_id}_{self.title}"


class Comment(TimeStampModel):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
