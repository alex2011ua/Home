from django.urls import include, path
from apps.spain.views import index, list_words, SearchWord, CompareWords, Settings, R_S, word_update, word_delete, word_translate

app_name = "spain"
urlpatterns = [
    path("api/", include("apps.spain.api.ruouter")),
    path("", index, name="spain_index"),
    path("list_words/", list_words, name="list_words"),
    path("search/", SearchWord.as_view(), name="SearchWord"),
    path("compare/", CompareWords.as_view(), name="CompareWords"),
    path("settings/", Settings.as_view(), name="settings"),
    path("r_s/", R_S.as_view(), name="r_s"),
    path("list_words/<int:id>/", word_update, name="update"),
    path("list_words/del/<int:id>/", word_delete, name="delete"),
    path("test_translate/<str:word>", word_translate, name="test_translate")
    ]