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

from .models import Menu, CartItem

# for stripe
import stripe
from django.conf import settings
from django.views import View
from django.views.generic import TemplateView


# Create your views here.
def index(request):
    menus = Menu.objects.all()
    return render(request, "restr/index.html", {"menus": menus})


# def productDetail(request):
#     return HttpResponseRedirect(reverse("restr:productDetail"))


# def userRegister(request):
#     # return render(request, "restr/userRegister.html")
#     return render(request, "restr/index.html")


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

    return render(request, "restr/ownerRegister.html", context)


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

    return render(request, "restr/ownerLogin.html")


def logoutUser(request):
    logout(request)
    return render(request, "restr/ownerLogin.html")


# Cart
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(
        request,
        "restr/cart.html",
        {"cart_items": cart_items, "total_price": total_price},
    )


def add_to_cart(request, product_id):
    product = Menu.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        product=product, user=request.user
    )
    cart_item.quantity += 1
    cart_item.save()
    return HttpResponseRedirect(reverse("restr:view_cart"))
    # return redirect("restr:view_cart")


def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect("restr:view_cart")


# Stripe payment
# from .models import Price

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateStripeCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(user=request.user)

        line_items = []

        for item in cart_items:
            line_items.append(
                {
                    "price_data": {
                        "currency": "inr",
                        "unit_amount": item.product.price * 100,
                        "product_data": {
                            "name": item.product.item,
                            "description": "placeholder definition for the product",
                            "images": [
                                "https://5.imimg.com/data5/TestImages/HT/HC/TC/SELLER-89159197/chhole-bhature-paddler-paper-500x500.jpg"
                            ],
                        },
                    },
                    "quantity": item.quantity,
                }
            )

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url="http://localhost:8000/success/",
            cancel_url="http://localhost:8000/cancel/",
        )

        return redirect(checkout_session.url)


class SuccessView(TemplateView):
    template_name = "restr/success.html"


class CancelView(TemplateView):
    template_name = "restr/cancel.html"
