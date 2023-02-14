from django.urls import include, path

from english.view_game import GenrundGame
from english.views import (
    E_R,
    R_E,
    CompareWords,
    Repeat,
    SearchWord,
    Settings,
    clear_control,
    clear_learned,
    index,
    list_words,
    mod,
    test,
    word_delete,
    word_update,
)

app_name = "english"
urlpatterns = [
    path("api/", include("english.api.ruouter")),
    path("", index, name="english_index"),
    path("settings/", Settings.as_view(), name="settings"),
    path("clear/", clear_control, name="clear"),
    path("clear_learned/", clear_learned, name="clear_learned"),
    path("test/", test, name="test"),
    path("list_words/", list_words, name="list_words"),
    path("list_words/<int:id>/", word_update, name="update"),
    path("list_words/del/<int:id>/", word_delete, name="delete"),
    path("e_r/mod/", mod),
    path("e_r/", E_R.as_view(), name="e_r"),
    path("r_e/mod/", mod),
    path("r_e/", R_E.as_view(), name="r_e"),
    path("search/", SearchWord.as_view(), name="SearchWord"),
    path("compare/", CompareWords.as_view(), name="CompareWords"),
    path("game/", GenrundGame.as_view(), name="game"),
    path("repeat/", Repeat.as_view(), name="repeat"),
]
