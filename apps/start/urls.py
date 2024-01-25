from django.urls import include, path

from .start_views import IndexView, EmailFormSabmit


app_name = "start"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("email_form_submit/", EmailFormSabmit.as_view(), name="index"),

]
