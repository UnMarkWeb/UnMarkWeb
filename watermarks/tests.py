from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AuthViewsTestCase(TestCase):
    def test_signup_get(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sing_up/sing_up.html")

    def test_signup_post_success(self):
        response = self.client.post(
            reverse("signup"),
            {
                "name": "Jane Doe",
                "email": "jane@example.com",
                "password": "strongpassword123",
                "terms": "on",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(email="jane@example.com").exists())
        user = User.objects.get(email="jane@example.com")
        self.assertEqual(user.first_name, "Jane")
        self.assertEqual(user.last_name, "Doe")
        # Ensure user is authenticated in session
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

    def test_signup_post_duplicate_email(self):
        User.objects.create_user(username="jane@example.com", email="jane@example.com", password="password123")
        response = self.client.post(
            reverse("signup"),
            {
                "name": "Jane Doe",
                "email": "jane@example.com",
                "password": "strongpassword123",
                "terms": "on",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ja existeix un compte")

    def test_signup_post_missing_terms(self):
        response = self.client.post(
            reverse("signup"),
            {
                "name": "Jane Doe",
                "email": "jane2@example.com",
                "password": "strongpassword123",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email="jane2@example.com").exists())

    def test_login_post_success(self):
        User.objects.create_user(username="jane@example.com", email="jane@example.com", password="password123")
        response = self.client.post(
            reverse("login"),
            {
                "email": "jane@example.com",
                "password": "password123",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(email="jane@example.com")
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

    def test_login_post_invalid(self):
        response = self.client.post(
            reverse("login"),
            {
                "email": "nobody@example.com",
                "password": "wrongpassword",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Correu o contrasenya incorrectes")

    def test_logout(self):
        user = User.objects.create_user(username="jane@example.com", email="jane@example.com", password="password123")
        self.client.force_login(user)
        response = self.client.get(reverse("logout"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_language_switching_es_and_en(self):
        # Switch to Spanish
        response = self.client.post(reverse("set_language"), {"language": "es"}, follow=True)
        self.assertEqual(response.status_code, 200)
        landing_es = self.client.get(reverse("landing_page"))
        self.assertContains(landing_es, "Protege y Limpia tus Imágenes")

        # Switch to English
        response = self.client.post(reverse("set_language"), {"language": "en"}, follow=True)
        self.assertEqual(response.status_code, 200)
        landing_en = self.client.get(reverse("landing_page"))
        self.assertContains(landing_en, "Protect and Clean your Images")
        
        login_en = self.client.get(reverse("login"))
        self.assertContains(login_en, "Welcome back")
        
        signup_en = self.client.get(reverse("signup"))
        self.assertContains(signup_en, "Create an account")
