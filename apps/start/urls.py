from django.urls import include, path

from .start_views import IndexView, EmailFormSabmit, Portfolio


app_name = "start"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("portfolio/<str:job>/", Portfolio.as_view(), name="portfolio"),


    path("email_form_submit/", EmailFormSabmit.as_view(), name="index"),

]
