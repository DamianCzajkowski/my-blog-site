from apps.post.models import Category, Post, Tag, Comment
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from functools import partial
from django.db.models.functions import Substr
from django.http import HttpResponseRedirect
from django.urls import reverse
from apps.user.models import User


def index(request):
    posts = (
        Post.objects.all()
        .prefetch_related("tags")
        .select_related("user_id")
        .annotate(Count("comments"))
    )
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(
        request, "index.html", {"posts": posts, "categories": categories, "tags": tags}
    )


def about(request):
    return render(request, "about.html")


def blog(request):
    posts = (
        Post.objects.all()
        .prefetch_related("tags")
        .select_related("user_id")
        .annotate(Count("comments"))
    )
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(
        request, "blog.html", {"posts": posts, "categories": categories, "tags": tags}
    )


def contact(request):
    return render(request, "contact.html")


def post_details(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(
        request,
        "post-details.html",
        {"post": post, "categories": categories, "tags": tags},
    )


def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = get_object_or_404(User, pk=1)
    Comment.objects.create(post_id=post, content=request.POST["message"], user_id=user)
    return HttpResponseRedirect(reverse("post-details", args=(post_id,)))
