from apps.post.models import Category, Post, Tag, Comment
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse
from apps.user.models import User
from apps.post import forms as post_forms
from django.core.paginator import Paginator


def index(request):
    posts = (
        Post.objects.all()
        .prefetch_related("tags")
        .select_related("user_id")
        .filter(is_public=True)
        .annotate(Count("comments"))[:3]
    )

    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(
        request, "index.html", {"posts": posts, "categories": categories, "tags": tags}
    )


def search_posts(request):
    query = request.GET.get("q")
    posts = (
        Post.objects.all()
        .prefetch_related("tags")
        .select_related("user_id")
        .annotate(Count("comments"))
        .filter(title__icontains=query)
    )
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(
        request, "blog.html", {"posts": posts, "categories": categories, "tags": tags}
    )


def add_post(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    form = post_forms.PostForm()
    if request.method == "POST":
        form = post_forms.PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user
            post.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse("post-details"), args=(post.id))

    return render(request, "add_post.html", {"form": form})


def blog(request, page=1):
    tag_id = request.GET.get("tag_id")
    category_id = request.GET.get("category_id")
    posts = (
        Post.objects.all()
        .prefetch_related("tags")
        .select_related("user_id")
        .annotate(Count("comments"))
    )
    if tag_id:
        posts = posts.filter(tags__id__exact=tag_id)
    if category_id:
        posts = posts.filter(category__id__exact=category_id)

    categories = Category.objects.all()
    tags = Tag.objects.all()
    paginator = Paginator(posts, 5)
    page_obj = paginator.get_page(page)
    return render(
        request,
        "blog.html",
        {"page_obj": page_obj, "categories": categories, "tags": tags},
    )


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
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    Comment.objects.create(
        post_id=post, content=request.POST["message"], user_id=request.user
    )
    return HttpResponseRedirect(reverse("post-details", args=(post_id,)))
