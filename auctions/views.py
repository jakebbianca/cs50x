from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing
from .forms import ListingForm


def index(request):
    return render(request, "auctions/index.html", 
        {'listings': Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def new_listing(request):
    if request.method == "POST":
        
        form = ListingForm(request.POST)

        if form.is_valid:
            title = request.POST["title"]
            description = request.POST["description"]
            price = request.POST["price"]
            url = request.POST["img_url"]
            category = request.POST["category"]
            seller = request.user

            new = Listing.objects.create(
                title = title,
                description = description,
                price = price,
                img_url = url,
                category = category,
                seller = seller,
            )
            new.save()

            return HttpResponseRedirect(reverse("index"))

        else:
            form = ListingForm(request.POST)
            print(form.errors)

            return render(request, "auctions/new_listing.html", {"form": form})

    else:
        form = ListingForm()

        return render(request, "auctions/new_listing.html", {"form": form})


@login_required
def listing(request):
    return render(request, "auctions/listing.html")