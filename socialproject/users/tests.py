from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import UserRegistartionForm
from .models import Profile


class RegistrationFormTests(TestCase):
    def test_password_confirmation_must_match(self):
        form = UserRegistartionForm(data={
            "username": "newuser",
            "email": "new@example.com",
            "first_name": "New",
            "password": "pass12345",
            "password2": "different",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_registration_email_must_be_unique(self):
        User.objects.create_user(username="existing", email="same@example.com", password="pass12345")

        form = UserRegistartionForm(data={
            "username": "newuser",
            "email": "same@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "pass12345",
            "password2": "pass12345",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)


class DiscoveryTests(TestCase):
    def setUp(self):
        self.creator = User.objects.create_user(username="creator", password="pass12345")
        self.viewer = User.objects.create_user(username="viewer", password="pass12345")
        Profile.objects.create(user=self.creator, bio="Landscape photos")
        Profile.objects.create(user=self.viewer)
        self.client.force_login(self.viewer)

    def test_search_users_finds_username(self):
        response = self.client.get(reverse("search_users"), {"q": "creat"})

        self.assertContains(response, "creator")
        self.assertNotContains(response, "Landscape photos")


class FollowTests(TestCase):
    def setUp(self):
        self.creator = User.objects.create_user(username="creator", password="pass12345")
        self.viewer = User.objects.create_user(username="viewer", password="pass12345")
        Profile.objects.create(user=self.creator)
        Profile.objects.create(user=self.viewer)
        self.client.force_login(self.viewer)

    def test_user_can_follow_and_unfollow_profile(self):
        response = self.client.post(
            reverse("toggle_follow", args=[self.creator.username]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["is_following"])
        self.assertEqual(response.json()["followers_count"], 1)

        response = self.client.post(
            reverse("toggle_follow", args=[self.creator.username]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["is_following"])
        self.assertEqual(response.json()["followers_count"], 0)

    def test_user_cannot_follow_self(self):
        response = self.client.post(
            reverse("toggle_follow", args=[self.viewer.username]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 400)
