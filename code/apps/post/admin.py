from apps.post.models import Comment, Post, Tag, Category
from django.contrib import admin

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Category)
