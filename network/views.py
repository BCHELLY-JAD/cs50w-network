import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    if request.method == 'GET': 
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)

    elif request.method == 'POST': 
        user = request.user
        post_content = request.POST["post_content"]
        information = Post.objects.create(post_owner=user, post_content=post_content)
        information.save()
        

    return render(request, "network/index.html", { 
        'posts' : posts,
    
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


#show the profile of each user when i click on his name
def profile(request, user_id): 

    person = Post.objects.filter(post_owner = user_id).order_by('-timestamp')    
    if request.method == 'GET': 
        paginator = Paginator(person, 10)
        page_number = request.GET.get('page')
        person = paginator.get_page(page_number)

        prof = User.objects.get(pk=user_id)
        return render(request, "network/profile.html", { 
            'person' : person,
            'followers_num': prof.count_followers,
            'following_num': prof.count_following,
            
        })


#display all posts of the users that i follow
def following_page(request):
    
    following = request.user.following.all()
    follposts = Post.objects.filter(post_owner__in=following).order_by('-timestamp')


    paginator = Paginator(follposts, 10)
    page_number = request.GET.get('page')
    follposts = paginator.get_page(page_number)
    
    return render(request, "network/follpage.html", { 
        'follposts' : follposts
        
    })


#function for follow/unfollow 
def follow(request, user_id): 
    profile_owner = User.objects.get(pk = user_id)

    if request.user in profile_owner.followers.all(): 
        request.user.following.remove(profile_owner)

    else: 
        request.user.following.add(profile_owner)
    
    return HttpResponseRedirect(reverse('profile', args=(user_id,)))


# like/unlike 

def like(request, post_id): 

    if request.method == 'PUT':
        post = Post.objects.get(pk=post_id) 
        print(post)
        if request.user in post.likes.all(): 
            post.likes.remove(request.user)
        else: 
            post.likes.add(request.user)
        post.save()
        return HttpResponse(status=204)


def edit(request, post_id):
    if request.method == 'PUT':

        data = json.loads(request.body)
        post = Post.objects.get(pk=data["post_id"])
        print(post)
        post_content  = data["post_content"]
        post.post_content = post_content 
        post.save()
        return JsonResponse({ 
            "post_content": post_content 
        }, status=200)


