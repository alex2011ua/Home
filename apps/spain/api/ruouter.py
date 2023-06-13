from django.urls import path

from apps.spain.api import views

urlpatterns = [
    path("repeat_words/", views.RepeatWordListView.as_view()),
    path("r_s_words/", views.REWordListView.as_view()),
    path("word/<int:pk>/", views.WordRUD.as_view(), name="wordRUD"),

]
