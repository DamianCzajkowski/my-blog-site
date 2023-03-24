from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

from . import forms


def login_page(request):
    form = forms.LoginForm()
    message = ""
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                message = "Login failed!"

    return render(
        request, "auth/login.html", context={"form": form, "message": message}
    )


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def signup_page(request):
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    return render(request, "auth/signup.html", context={"form": form})
