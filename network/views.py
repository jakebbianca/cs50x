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


@login_required
def profile(request, profile_id):

    user_id = request.user

    return render(request, "network/profile.html", {
        "profile_id": profile_id, "user_id": user_id})


def user(request, user_id):

    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)

    user = User.objects.get(pk=user_id)

    return JsonResponse(user.serialize(), safe=False, status=200)


@csrf_exempt
@login_required
def following(request):

    # retrieve Follows objects for all cases where current user is an active follower
    followed_qs = Follows.objects.filter(
        follower=request.user,
        active_bool=True
    )

    # create a list of ids of users followed by the current user
    users_followed = []
    
    for item in followed_qs:
        users_followed.append(item.following.id)

    print(f"IDs of users followed: {users_followed}")
    print(f"Type of users_followed: {type(users_followed)}")
    if len(users_followed) == 0:
        users_followed = None

    return render(request, "network/following.html",
                {"users_followed": users_followed})


# under construction
def following_API(request, other_user_id=None):

    if other_user_id is not None:
        other_user = User.objects.get(pk=other_user_id)
        user_follows = Follows.objects.filter(user=other_user, active_bool=True)
    else:
        user_follows = Follows.objects.filter(user=request.user, active_bool=True)

    return JsonResponse(user_follows.serialize(), safe=False, status=200)


    

@csrf_exempt
@login_required
def new(request):

    # Creating a new post must be via POST method
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # store data sent via fetch call to a variable
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


@csrf_exempt
def posts(request, poster_id=None):

    if request.method != "POST":
        return JsonResponse({"error": "GET or POST request required."}, status=400)

    # load data from body of POST request and store
    data = json.loads(request.body)
    posters_ids = data.get("posters_ids")

    # if a single poster is specified, load only that user's posts
    if poster_id is not None:
        # get specific page of posts
        poster = User.objects.get(pk=poster_id)
        posts = Post.objects.filter(poster=poster)

    # if multiple user ids are provided, load their posts
    elif len(posters_ids) != 0:
        # get followed users using poster ids, return error if failed
        try:
            posters = User.objects.filter(pk__in=posters_ids)
        except:
            print("Error getting posters")
            return JsonResponse(
                {"error": "Failed to get list of followed users."},
                status=400)

        if not posters:
            return JsonResponse([], safe=False, status=200)
        
        # get all posts from all followed users, return error if failed
        try:
            posts = Post.objects.filter(poster__in=posters)
        except:
            print("Error getting posts")
            return JsonResponse(
                {"error": "Failed to get posts from followed users."},
                status=400
            )

    #if no user ids are provided, load all posts from all users
    else:
        posts = Post.objects.all()


    # order the posts in reverse-chronological order
    posts = posts.order_by("-id").all()

    # check for pagination error, NEXT and PREV
    if data.get("clicked_next") == True and data.get("clicked_prev") == True:
        return JsonResponse(
            {"error": "Request included NEXT and PREV = True"},
            status=400
        )


    # WORKING ON THIS
    # check if user is loading the next page
    if data.get("clicked_next") == True:
        next_cursor = data.get("next_cursor")

    elif data.get("clicked_prev") == True:
        prev_cursor = data.get("prev_cursor")

    else:
        pass

    # get prev page cursor
    # prev-cursor-post = posts.filter(id__lt=)

    # filter posts by id <= id of next page cursor
    # return 11 items (10 + 1 for next cursor)
    # posts = posts.filter(id__gte=next_cursor)[:11]
    # get new next_cursor to send to template
    # try:
    #   new_next_cursor = posts[10].id
    # except:
    #   new_next_cursor = None


    return JsonResponse([post.serialize() for post in posts], safe=False, status=200)


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