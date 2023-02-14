from django.contrib.auth import views
from django.urls import include, path

from myviberbot.views import trx_bot

from .start_views import IndexView, RegisterView, VideoRating

urlpatterns = [

    path("avto/", include("selection_avto.urls")),
    path("", IndexView.as_view(), name="index"),
    path("accounts/login/", views.LoginView.as_view(), name="login"),
    path("accounts/logout/", views.LogoutView.as_view(), name="logout"),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("webhook2020/", trx_bot),
    path("english/", include("english.urls", namespace="english")),


]
