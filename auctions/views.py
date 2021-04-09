from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid
from .forms import ListingForm, BidForm


def index(request):
    return render(request, "auctions/index.html", 
        {"listings": Listing.objects.all().filter(status=True)
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
def listings(request, listing_id):

    if request.method == "POST":

        form = BidForm(request.POST)
        if form.is_valid:
            # variables for new Bid object
            bid = request.POST["bid"]
            listing = Listing.objects.get(pk=listing_id)
            # check if bid > previous bid or >= starting price if no other bids
            # if true, render template again with error message
            # if not, insert new Bid and update current Listing 'listing'
            bid_count = Bid.objects.all().filter(listing=listing_id).count()
            current_price = Listing.objects.all().filter(id=listing_id).first().price
            if (bid_count > 0 and float(bid) <= current_price) or (bid_count == 0 and float(bid) < current_price):
                listing = Listing.objects.all().filter(id=listing_id).first()
                bid_error = "Any bid placed must be greater than the previously leading bid orat least as great as the starting price if no other bids have been placed."
                return render(request, "auctions/listing.html", {"listing": listing, "form": form, "bid_count": bid_count, 
                                                                "is_leader": False, "bid_error": bid_error})
            
            else:

                new = Bid.objects.create(
                    bid = bid,
                    listing = listing,
                    bidder = request.user
                )
                new.save()

                listing.price = bid
                listing.save()

                return HttpResponseRedirect(reverse("listings", args=[listing_id]))

        else:
            print(form.errors)
            return render(request, "auctions/listing.html", {"listing": listing})

    else:
        if Listing.objects.all().filter(id=listing_id).count() == 0:
            return HttpResponseRedirect(reverse("dne"))

        bid_count = Bid.objects.all().filter(listing=listing_id).count()
        # NEED TO FIX -- is_leader not displaying leader on GET
        if bid_count > 0:
            leader = Bid.objects.all().filter(listing=listing_id).last()
            if leader.id == request.user.id:
                is_leader = True
            else:
                is_leader = False
        else:
            is_leader = False
        
        listing = Listing.objects.all().filter(id=listing_id).first()
        form = BidForm()
        return render(request, "auctions/listing.html", {"listing": listing, "form": form, "bid_count": bid_count,
                                                        "is_leader": is_leader, "bid_error": ""})


def dne(request):
    return render(request, "auctions/dne.html")