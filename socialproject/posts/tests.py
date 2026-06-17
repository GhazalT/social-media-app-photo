from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import CommentForm
from .models import Comment, Post


class CommentFormTests(TestCase):
    def test_comment_author_is_not_public_form_field(self):
        form = CommentForm()

        self.assertEqual(list(form.fields), ["body"])


class PostInteractionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ava", password="pass12345")
        self.post = Post.objects.create(
            user=self.user,
            title="Morning light",
            image="images/test.jpg",
            caption="First post",
        )
        self.client.force_login(self.user)

    def test_like_endpoint_returns_json_for_ajax_requests(self):
        response = self.client.post(
            reverse("like"),
            {"post_id": self.post.id},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "liked": True,
            "like_count": 1,
            "like_text": "1 like",
        })

    def test_feed_comment_uses_logged_in_user(self):
        response = self.client.post(
            reverse("feed"),
            {
                "post_id": self.post.id,
                "body": "Looks great",
                "posted_by": "spoofed",
            },
        )

        self.assertRedirects(response, reverse("feed"))
        comment = Comment.objects.get()
        self.assertEqual(comment.posted_by, self.user.username)

    def test_owner_can_delete_post(self):
        response = self.client.post(
            reverse("post_delete", args=[self.post.id]),
            {"next": reverse("feed")},
        )

        self.assertRedirects(response, reverse("feed"))
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_other_user_cannot_delete_post(self):
        other_user = User.objects.create_user(username="noor", password="pass12345")
        self.client.force_login(other_user)

        response = self.client.post(reverse("post_delete", args=[self.post.id]))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())
