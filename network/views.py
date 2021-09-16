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
        user_follows = Follows.objects.filter(
            user=other_user,
            active_bool=True
        )
    else:
        user_follows = Follows.objects.filter(
            user=request.user,
            active_bool=True
        )

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
def posts(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # load data from body of POST request and store
    data = json.loads(request.body)
    poster_id = data.get("poster_id")
    posters_ids = data.get("posters_ids")

    # if a single poster is specified, load only that user's posts
    if poster_id is not None:

        # find specified poster and get qs for their posts
        poster = User.objects.get(pk=poster_id)
        posts = Post.objects.filter(poster=poster)

    # if multiple user ids are provided, load their posts
    # for following page
    elif posters_ids is not None:

        # get followed users using poster ids, return error if failed
        try:
            posters = User.objects.filter(pk__in=posters_ids)
        except:
            print("Error getting posters.")
            return JsonResponse(
                {"error": "Failed to get list of followed users."},
                status=400)

        # if for some reason no posters are found, return no posts
        if not posters:
            return JsonResponse([], safe=False, status=200)
        
        # get qs of all posts from all followed users, return error if failed
        try:
            posts = Post.objects.filter(poster__in=posters)
        except:
            print("Error getting posts.")
            return JsonResponse(
                {"error": "Failed to get posts from followed users."},
                status=400
            )

    #if no user ids are provided, load all posts from all users
    else:
        posts = Post.objects.all()

    # check for pagination error, NEXT and PREV
    # if unable to access either click variable, return an error
    try:
        if (data.get("clicked_next") == True and 
            data.get("clicked_prev") == True):
            return JsonResponse(
                {"error": "Request included NEXT and PREV = True"},
                status=400
            )
    except:
        return JsonResponse(
            {"error": "Could not find one of clicked_next or clicked_prev"},
            status=400
        )

    # order posts in reverse-chronological order
    posts = posts.order_by("-id").all()

    # check if user is loading the prev page
    if bool(data.get("clicked_prev")) is True:

        # get prev cursor from POST request
        prev_cursor = data.get("prev_cursor")

        # define qs for posts to load and new prev cursor
        p1 = posts.filter(pk__gte=prev_cursor)
        n_p1 = p1.count()


        # if less than 11 posts are retrieved, load first page of posts
        # if 11 posts are retrieved, store cursor and posts to display
        if n_p1 < 11:

            new_prev_cursor = None
            first_page_posts = posts[:11]

            new_next_cursor = first_page_posts[10].id
            posts_to_display = first_page_posts[:10]
        
        else:
            
            p1_pc_offset = n_p1 - 11
            p1_ptd_offset = n_p1 - 10
            new_prev_cursor = posts[p1_pc_offset].id
            posts_to_display = posts[p1_ptd_offset:p1_ptd_offset+10]
            print(posts_to_display)

            # define qs for and store new next cursor
            p2 = posts.filter(pk__lt=prev_cursor)
            new_next_cursor = p2[0].id


    elif bool(data.get("clicked_next")) is True:

        next_cursor = data.get("next_cursor")

        # define qs for posts to load and new next cursor
        p1 = posts.filter(pk__lte=next_cursor)
        p1 = p1[:11]

        # if less than 11 posts are retrieved, last page of posts
        # if 11 posts are retrieved, store cursor and posts to display
        if len(p1) < 11:
            new_next_cursor = None
            posts_to_display = p1
        else:
            new_next_cursor = p1[10].id
            posts_to_display = p1[:10]

        # define qs for and store new prev cursor
        p2 = posts.filter(pk__gt=next_cursor)
        n_p2 = p2.count() - 1
        new_prev_cursor = p2[n_p2].id

    # if loading fresh post page (no next or prev)
    # load newest 10 posts, get next cursor
    else:

        # load 1st 11 posts (10 to display, one for next cursor)
        posts = posts[:11]

        # set prev cursor to None since we are loading first page
        new_prev_cursor = None

        # if less than 11 posts are loaded, load available without cursor
        # if 11 posts retrieved, store cursor and posts to display
        if len(posts) < 11:
            new_next_cursor = None
            posts_to_display = posts
        else:
            new_next_cursor = posts[10].id
            posts_to_display = posts[:10]


    posts_serialized = [post.serialize() for post in posts_to_display]
    # define and encode data for JSON response
    json_response_data = {
        "posts": posts_serialized,
        "posterID": poster_id,
        "postersIDs": posters_ids,
        "prevCursor": new_prev_cursor,
        "nextCursor": new_next_cursor
    }

    # return JSON data per fetch request
    return JsonResponse(
        json_response_data,
        status=200)


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