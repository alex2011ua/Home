from django.contrib import admin

from english.models import WordParams, Words


@admin.register(Words)
class WordsAdmin(admin.ModelAdmin):
    list_display = ("lesson", "english", "russian", "repeat_learn", "important", "heavy", "learned", "info")

    list_filter = ("lesson", "heavy", "learned", "important", "repeat_learn", "phrasal_verbs", "irregular_verbs")


@admin.register(WordParams)
class WordsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "learned",
        "heavy",
        "lesson_1",
        "lesson_2",
        "lesson_3",
        "lesson_4",
        "lesson_5",
        "lesson_6",
        "lesson_7",
        "lesson_8",
        "lesson_9",
        "lesson_10",
        "lesson_11",
        "lesson_12",
        "lesson_13",
        "level_1",
        "level_2",
        "level_3",
        "level_4",
        "level_5",
        "lesson_0",
        "phrasal_verbs",
        "irregular_verbs",
        "control_state",

    )

    list_filter = ()
