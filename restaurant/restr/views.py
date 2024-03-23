from django.shortcuts import render, HttpResponseRedirect, redirect

# from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse

# for login
from django.contrib.auth import authenticate, login, logout

# TODO: read about ModelManager
from django.contrib.auth.models import Group

# flash message
from django.contrib import messages

# for form
# from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm

# for importing decorators from decorators.py file and using above the loginPage() function
from .decorators import unauthenticated_user


# Create your views here.
def index(request):
    return render(request, "restr/index.html")


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            owner = Group.objects.get(name="owner")

            user.groups.add(owner)
            user.save()

            messages.success(
                request, "Account created successfully for " + user.username
            )
            return HttpResponseRedirect(reverse("restr:login"))

    context = {"form": form}

    return render(request, "restr/register.html", context)


@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request, username=username, password=password
        )  # matching username and password of login input field ans stored username from database that is registered

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("restr:index"))
        else:
            messages.info(request, "Username or password is incorrect")

    return render(request, "restr/login.html")


def logoutUser(request):
    logout(request)
    return render(request, "restr/login.html")
