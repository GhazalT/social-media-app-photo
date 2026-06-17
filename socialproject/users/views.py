from django.contrib.auth.models import User
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LoginForm, UserRegistartionForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import UserEditForm, ProfileEditForm
from posts.models import Post


# Create your views here.
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data["username"], password=data["password"])
            if user is not None:
                login(request, user)
                messages.success(request, "Welcome back.")
                return redirect("feed")
            else:
                form.add_error(None, "Invalid username or password.")
    else:   
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})

@login_required
def index(request):
    current_user = request.user
    posts = Post.objects.filter(user=current_user).order_by("-created")
    profile, _ = Profile.objects.get_or_create(user=current_user)

    return render(request, "users/index.html", {
        "posts": posts,
        "profile": profile,
        "followers_count": current_user.followers.count(),
        "following_count": profile.following.count(),
    })


def register(request):
    if request.method == 'POST':
        user_form = UserRegistartionForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            messages.success(request, "Account created. You can log in now.")
            return redirect("login")
    else:
        user_form = UserRegistartionForm()
    return render(request, 'users/register.html', {'user_form': user_form})

@login_required
def edit(request):
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated.")
            return redirect("index")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)        
    return render(request, 'users/edit.html', {"user_form": user_form, "profile_form": profile_form})


@login_required
def search_users(request):
    query = request.GET.get("q", "").strip()
    users = User.objects.none()
    suggestions = User.objects.none()

    if query:
        users = (
            User.objects
            .select_related("profile")
            .annotate(post_count=Count("post"))
            .filter(username__icontains=query)
            .order_by("username")[:30]
        )
    else:
        suggestions = (
            User.objects
            .exclude(id=request.user.id)
            .select_related("profile")
            .annotate(post_count=Count("post"))
            .order_by("-date_joined")[:8]
        )

    return render(request, "users/search.html", {
        "query": query,
        "users": users,
        "suggestions": suggestions,
    })


@login_required
def profile_detail(request, username):
    profile_user = get_object_or_404(User.objects.select_related("profile"), username=username)
    profile, _ = Profile.objects.get_or_create(user=profile_user)
    viewer_profile, _ = Profile.objects.get_or_create(user=request.user)
    posts = (
        Post.objects
        .filter(user=profile_user)
        .prefetch_related("liked_by")
        .order_by("-created")
    )

    return render(request, "users/profile_detail.html", {
        "profile_user": profile_user,
        "profile": profile,
        "posts": posts,
        "followers_count": profile_user.followers.count(),
        "following_count": profile.following.count(),
        "is_following": viewer_profile.following.filter(id=profile_user.id).exists(),
    })


@login_required
def toggle_follow(request, username):
    profile_user = get_object_or_404(User, username=username)
    viewer_profile, _ = Profile.objects.get_or_create(user=request.user)
    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"

    if request.method != "POST":
        if is_ajax:
            return JsonResponse({"error": "POST required."}, status=405)
        return redirect("profile_detail", username=username)

    if profile_user == request.user:
        messages.error(request, "You cannot follow your own profile.")
        if is_ajax:
            return JsonResponse({"error": "You cannot follow your own profile."}, status=400)
        return redirect("profile_detail", username=username)

    if viewer_profile.following.filter(id=profile_user.id).exists():
        viewer_profile.following.remove(profile_user)
        is_following = False
    else:
        viewer_profile.following.add(profile_user)
        is_following = True

    followers_count = profile_user.followers.count()

    if is_ajax:
        return JsonResponse({
            "is_following": is_following,
            "followers_count": followers_count,
            "button_text": "Following" if is_following else "Follow",
        })

    return redirect("profile_detail", username=username)


