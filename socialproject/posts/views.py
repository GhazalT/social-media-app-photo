from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import CommentForm, PostCreateForm
from .models import Post


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            messages.success(request, "Post created successfully.")
            return redirect("feed")
    else:
        form = PostCreateForm()

    return render(request, "posts/create.html", {"form": form})


@login_required
def feed(request):
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            post_id = request.POST.get("post_id")

            if post_id:
                post = get_object_or_404(Post, id=post_id)
                new_comment.post = post
                new_comment.posted_by = request.user.get_username()
                new_comment.save()
                messages.success(request, "Comment added successfully.")
            else:
                messages.error(request, "Post not found.")
        else:
            messages.error(request, "Comment cannot be empty.")

        return redirect("feed")

    comment_form = CommentForm()
    posts = (
        Post.objects
        .select_related("user", "user__profile")
        .prefetch_related("liked_by", "comments")
        .order_by("-created")
    )

    return render(request, "posts/feed.html", {
        "posts": posts,
        "logged_user": request.user,
        "comment_form": comment_form,
    })


@login_required
@require_POST
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user_id != request.user.id:
        return HttpResponseForbidden("You cannot delete this post.")

    image = post.image
    post.delete()
    if image:
        image.delete(save=False)

    messages.success(request, "Post deleted successfully.")

    next_url = request.POST.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(next_url)

    return redirect("feed")


def _like_count_label(count):
    if count == 0:
        return ""
    if count == 1:
        return "1 like"
    return f"{count} likes"


@login_required
def like_post(request):
    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"

    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post = get_object_or_404(Post, id=post_id)

        if post.liked_by.filter(id=request.user.id).exists():
            post.liked_by.remove(request.user)
            liked = False
        else:
            post.liked_by.add(request.user)
            liked = True

        if is_ajax:
            like_count = post.liked_by.count()
            return JsonResponse({
                "liked": liked,
                "like_count": like_count,
                "like_text": _like_count_label(like_count),
            })

    elif is_ajax:
        return JsonResponse({"error": "POST required."}, status=405)

    return redirect("feed")
