import os

from django.urls import include, path

from . import views
from .ajax import ajax, ajax_analiz, ajax_zvit

token = os.getenv("TOKEN", os.environ.get("TOKEN"))

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("analiz/ajax/analiz/", ajax_analiz),
    path("analiz/ajax/zvit/", ajax_zvit),
    path("clear_baze/", views.clear_baze),
    path("{}/".format(token), views.get_bot_message, name="get_bot_message"),
    path("analiz/", views.AnalizView.as_view(), name="analiz"),
    path("ajax/", ajax),
]
