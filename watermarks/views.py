from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages


def landing_page(request):
    if request.user.is_authenticated:
         return redirect("dashboard_reload")
    return render(request, "landing_page/landing_page.html")

def dashboard_reload(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "dashboard/dashboard.html")

def login(request):
    if request.user.is_authenticated:
        return redirect("landing_page")

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        remember_me = request.POST.get("remember-me")

        # Try authenticating directly by username (stored as email)
        user = authenticate(request, username=email, password=password)
        if user is None:
            # In case username is different from email, search by email
            try:
                user_obj = User.objects.get(email__iexact=email)
                user = authenticate(request, username=user_obj.username, password=password)
            except (User.DoesNotExist, User.MultipleObjectsReturned):
                user = None

        if user is not None:
            auth_login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            return redirect("landing_page")
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, "login/login.html", {"email": email})

    return render(request, "login/login.html")


def logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("landing_page")


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("landing_page")

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        terms = request.POST.get("terms")

        # Validation
        if not name or not email or not password:
            messages.error(request, "Please fill in all required fields.")
            return render(request, "sing_up/sing_up.html", {"name": name, "email": email})

        if not terms:
            messages.error(request, "You must agree to the Terms and Conditions.")
            return render(request, "sing_up/sing_up.html", {"name": name, "email": email})

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return render(request, "sing_up/sing_up.html", {"name": name, "email": email})

        if User.objects.filter(email__iexact=email).exists() or User.objects.filter(username__iexact=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, "sing_up/sing_up.html", {"name": name, "email": email})

        # Name parsing
        name_parts = name.split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Automatically log the user in after registration
        auth_login(request, user)
        messages.success(request, "Account created successfully! Welcome to UnMark.")
        return redirect("landing_page")

    return render(request, "sing_up/sing_up.html")