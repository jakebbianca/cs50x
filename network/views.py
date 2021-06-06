import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follows, Likes


# this will show ALL POSTS and New Post Form
def index(request):

    # authenticated users may view the index
    if request.user.is_authenticated:
            return render(request, "network/index.html")

    # everyone else required to log in
    else:
        return HttpResponseRedirect(reverse("login"))


@csrf_exempt
@login_required
def new(request):

    # Creating a new post must be via POST method
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # save data sent via fetch call to a variable
    data = json.loads(request.body)

    # store new post content in a variable
    content = data.get("content")
    # content must not be empty or only whitespace
    if not content or content.isspace():
        return JsonResponse({
            "error": "A new post must contain some content and must include at least one non-whitespace character."}, 
            status=400)

    #create and save a new Post object given the submitting user and the content of the post
    post = Post(
        poster=request.user,
        content=content
    )
    post.save()

    #return successful response once post is saved
    return JsonResponse({"message": "Post submitted successfully"}, status=201)


@csrf_exempt
@login_required
def post(request, post_id):
    
    # Editing or liking a post must be via PUT method
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    # confirm that post exists and store in variable if so, otherwise return error
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=400)

    # more TODO


def posts(request, poster=None):

    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)

    # if a poster is specified, load only that user's posts
    # if a poster is not specified, load all posts from all users
    if poster:
        posts = Post.objects.filter(poster=poster)
    else:
        posts = Post.objects.all()

    # order the posts in reverse-chronological order
    posts = posts.order_by("-post_datetime").all()
    return JsonResponse([post for post in posts], status=200)
    

    
    

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")