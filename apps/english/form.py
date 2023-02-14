from django import forms

from .models import WordParams, Words


class LoadWordsForm(forms.Form):
    file = forms.FileField(label="загрузить файл со словами")


class LoadWordForm(forms.ModelForm):
    class Meta:
        model = Words
        fields = (
            "lesson",
            "english",
            "russian",
            "info",
            "phrasal_verbs",
            "irregular_verbs",
        )
        labels = {
            "lesson": "lesson",
            "english": "english",
            "russian": "russian",
            "info": "info",
            "phrasal_verbs": "Только слова для экзамена",
            "irregular_verbs": "Только неправильные глаголы",
        }


class WordsParamForm(forms.ModelForm):
    class Meta:
        model = WordParams
        fields = (
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
            "only_important_words",
        )

        labels = {
            "learned": "Не показывать выученые слова",
            "heavy": "Только сложные слова",
            "lesson_0": "Слова без привязки к уроку",
            "phrasal_verbs": "Только слова для экзамена",
            "irregular_verbs": "Только неправильные глаголы",
            "only_important_words": "только важные слова",
        }


class SearchWordForm(forms.Form):
    word = forms.CharField(label="слово")


class CompareWordForm(forms.Form):
    first_word = forms.CharField(label="1 строка")
    second_word = forms.CharField(label="2 строка")
