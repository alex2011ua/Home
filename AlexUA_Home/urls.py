"""AlexUA_Home URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib.auth import views
from django.contrib import admin
from django.urls import path, include
from apps.start.start_views import RegisterView
from apps.start.start_views import EmailFormSabmit

urlpatterns = [
    path('admin/', admin.site.urls),
    path('english/', include("apps.english.urls", namespace="english")),
    path('spain/', include("apps.spain.urls", namespace="spain")),
    path("accounts/login/", views.LoginView.as_view(), name="login"),
    path("accounts/logout/", views.LogoutView.as_view(), name="logout"),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path('', include("apps.start.urls", namespace="start")),
    path("email_form_submit/", EmailFormSabmit.as_view(), name="index"),

]
