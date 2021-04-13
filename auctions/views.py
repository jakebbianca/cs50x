from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Watchlist
from .forms import ListingForm, BidForm


def index(request):
    return render(request, "auctions/index.html", 
        {"listings": Listing.objects.all().filter(status=True)
    })

@login_required
def watchlist(request):
    watchlist = Watchlist.objects.all().filter(user=request.user)
    listings = [k.listing for k in watchlist]
    return render(request, "auctions/watchlist.html", {"listings": listings})


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
    # when user submits new listing form, check if form is valid
    # if valid, create a new Listing and save to the db
    # if not valid, print errors and render new listing page again with information still filled in
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

    # on GET, render the new listing template with a blank ListingForm
    else:
        form = ListingForm()

        return render(request, "auctions/new_listing.html", {"form": form})


@login_required
def listings(request, listing_id):

    # define common variables for this view
    current_user = request.user
    listing = Listing.objects.get(pk=listing_id)
    if listing.seller == current_user:
        seller_check = True
    else:
        seller_check = False

    # check if listing is on user's watchlist
    try:
        watchlist = Watchlist.objects.get(user=current_user, listing=listing)
    except:
        wl_check = False
    else:
        wl_check = True


    if request.method == "POST":
        # when user presses 'watchlist' button on a given listing
        if "watch_button" in request.POST:
            # if listing is on user's watchlist, delete it
            # if not, create and save it
            if wl_check == False:
                new = Watchlist.objects.create(
                    user = current_user,
                    listing = listing
                )
                new.save()
            else:
                Watchlist.objects.get(pk=watchlist.id).delete()


        elif "bid_button" in request.POST:
            form = BidForm(request.POST)
            bid_count = Bid.objects.all().filter(listing=listing_id).count()
            current_price = Listing.objects.all().filter(id=listing_id).first().price
            # check if seller is trying to bid on their own item
            if seller_check is True:
                bid_error = "You cannot bid on your own listing."
                return render(request, "auctions/listing.html", {"listing": listing, "form": form, "bid_count": bid_count, 
                                                                    "is_leader": False, "bid_error": bid_error, "wl_check": wl_check,
                                                                    "seller_check": seller_check})
            # check bid for errors and submit if acceptable
            if form.is_valid:
                # variables for new Bid object
                bid = request.POST["bid"]
                # check if bid > previous bid or >= starting price if no other bids
                # if true, render template again with error message
                # if not, insert new Bid and update current Listing 'listing'
                if (bid_count > 0 and float(bid) <= current_price) or (bid_count == 0 and float(bid) < current_price):
                    listing = Listing.objects.all().filter(id=listing_id).first()
                    bid_error = "Any bid placed must be greater than the previously leading bid or at least as great as the starting price if no other bids have been placed."
                    return render(request, "auctions/listing.html", {"listing": listing, "form": form, "bid_count": bid_count, 
                                                                    "is_leader": False, "bid_error": bid_error, "wl_check": wl_check,
                                                                    "seller_check": seller_check})
                
                # once confirmed there are no errors, create/save new bid to db
                # also update current price on listing before reloading page
                else:

                    new = Bid.objects.create(
                        bid = bid,
                        listing = listing,
                        bidder = current_user
                    )
                    new.save()

                    listing.price = bid
                    listing.winner = current_user
                    listing.save()

        elif "close_button" in request.POST:
            # close the listing
            listing.status = False
            listing.save()

        # if post is successful, redirect to new instance of listing page
        return HttpResponseRedirect(reverse("listings", args=[listing_id]))

    # GET
    else:
        # check if listing exists in db; if not, redirect to 404 page
        if Listing.objects.all().filter(id=listing_id).count() == 0:
            return HttpResponseRedirect(reverse("dne"))

        bid_count = Bid.objects.all().filter(listing=listing).count()
        # NEED TO FIX -- is_leader not displaying leader on GET
        if bid_count > 0:
            leader = Bid.objects.all().filter(listing=listing).last()
            if leader.bidder.id == current_user.id:
                is_leader = True
            else:
                is_leader = False
        else:
            is_leader = False
        
        form = BidForm()
        return render(request, "auctions/listing.html", {"listing": listing, "form": form, "bid_count": bid_count,
                                                        "is_leader": is_leader, "bid_error": "", "wl_check": wl_check,
                                                        "seller_check": seller_check})


def categories(request):
    categories = Listing.CATEGORIES
    return render(request, "auctions/categories.html", {"categories": categories})


def category(request, key):
    categories = Listing.CATEGORIES
    for i, j in categories:
        if i == key:
            category_name = j
    if not category_name:
        return HttpResponseRedirect(reverse("dne"))
    listings = Listing.objects.all().filter(category=key, status=True)
    return render(request, "auctions/category.html", {"listings": listings, "category_name":category_name})


def dne(request):
    return render(request, "auctions/dne.html")