"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from watermarks.views import landing_page, login, logout, sign_up, dashboard_reload, support,state,faq,videos, forum

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", landing_page, name="landing_page"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("signup/", sign_up, name="signup"),
    path("dashboard/", dashboard_reload, name="dashboard_reload"),
    path("support/", support, name="support"),
    path("support/state/", state, name="state"),
    path("support/faq/", faq, name="faq"),
    path("support/videos/", videos, name="videos"),
    path("support/forum/", forum, name="forum"),
]
