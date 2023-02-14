from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .models import Words


class GenrundGame(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        return render(request, "english/play_gerund.html")

    @staticmethod
    def post(request):
        content = []
        words_all = Words.objects.filter(lesson=88)
        for _word in words_all:
            try:
                word, buttons = _word.english.split("-", 1)
                answer, russian = _word.russian.split("-", 1)
                buttons = buttons.split(",")
                buttons = list(map(str.strip, buttons))
            except ValueError as arr:
                print(arr)
                print(_word.english)
                continue
            d_word = {
                "word": word,
                "buttons": buttons,
                "answer": answer.strip(),
                "russian": russian,
                "id": _word.id,
            }
            content.append(d_word)
        return JsonResponse(content, safe=False)
