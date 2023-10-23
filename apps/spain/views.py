from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from apps.spain.form import CompareWordForm, LoadWordForm, LoadWordsForm, SearchWordForm, WordsParamForm
from apps.spain.models import WordParamsSpain, Words
from django.contrib.auth.models import User
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)

def index(request):
    """
    Выбор списка слов
    :param request:
    :return:
    """

    if request.method == "GET":
        try:
            user = User.objects.get_by_natural_key("test_user")
        except Exception:
            user = User.objects.create_user(
                "test_user",
                "test_user@gamil.com",
                password="asdf"
            )
        login(request, user)

        logger.warning(request.user)
        try:
            params = WordParamsSpain.objects.get(user=request.user)
        except:
            params = WordParamsSpain.objects.create(user=request.user)
        form_word_param = WordsParamForm(instance=params)
        all = WordParamsSpain.get_words(request.user.id)
        return render(
            request,
            "spain/base_spain.html",
            {"form_word_param": form_word_param, "params": params, "count": len(all)},
        )
    if request.method == "POST":
        params = WordParamsSpain.objects.get(user=request.user)
        form = WordsParamForm(request.POST, instance=params)
        if form.is_valid():
            form.save()
        return redirect("spain:spain_index")


def list_words(request):
    """
    list checking words
    :param request:
    :return:
    """
    if request.method == "GET":
        all = WordParamsSpain.get_words(request.user.id)
        return render(request, "spain/list_words.html", {"words": all, "count": len(all)})

class SearchWord(View):
    """
    search words in my bd
    """

    @staticmethod
    def get(request):
        form = SearchWordForm()
        return render(request, "spain/search_word.html", {"form": form})

    @staticmethod
    def post(request):
        form = SearchWordForm()
        input_word = request.POST.get("word")
        spain_words = Words.objects.filter(spain__icontains=input_word)
        russian_words = Words.objects.filter(russian__icontains=input_word)

        count = len(spain_words) + len(russian_words)

        return render(
            request,
            "spain/search_word.html",
            {
                "form": form,
                "spain_words": spain_words,
                "russian_words": russian_words,
                "count": count,
            },
        )


class CompareWords(View):
    """
    compare two lines to find differences
    """

    @staticmethod
    def get(request):
        form = CompareWordForm()
        return render(request, "spain/compare_word.html", {"form": form})

    @staticmethod
    def post(request):
        import difflib as df

        form = CompareWordForm()
        first_word = request.POST.get("first_word")
        second_word = request.POST.get("second_word")
        if first_word == second_word:
            answer = "Строки одинаковы"
        else:
            d = df.Differ()
            diff = d.compare(first_word, second_word)
            answer = "".join(diff)
        return render(
            request,
            "spain/compare_word.html",
            {
                "form": form,
                "answer": answer,
                "first_word": first_word,
                "second_word": second_word,
            },
        )


class Settings(LoginRequiredMixin, View):
    """
    Add new words
    """

    permission_required = "is_staff"

    @staticmethod
    def get(request):
        count = Words.objects.all().count()
        form_list_words = LoadWordsForm()
        form_word = LoadWordForm()
        return render(
            request,
            "spain/settings.html",
            {
                "form_word": form_word,
                "form_list_words": form_list_words,
                "count": count,
            },
        )

    @staticmethod
    def post(request):
        if request.POST.get("spain"):
            form = LoadWordForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect("spain:settings")
        if request.FILES.get("file"):
            name_file, _ = request.FILES.get("file").name.split(".")
            irregular_verbs = False

            try:
                lesson = int(name_file)
            except:
                lesson = 99

            if name_file == "irregular_verbs":
                irregular_verbs = True
            file_ = request.FILES.get("file").read()
            content = file_.decode("utf-8").split("\r\n")
            if len(content) < 2:  # git modify text file and delete \r
                content = file_.decode("utf-8").split("\n")
            for item in content:
                try:
                    item = item.strip()
                    item = item.replace("’", "'")

                    if ";" in item:
                        spain, russian = item.split(";", 1)
                    elif "•" in item:
                        spain, russian = item.split("•", 1)
                    elif "-" in item:
                        spain, russian = item.split("-", 1)
                    elif "," in item:
                        spain, russian = item.split(",", 1)

                    spain = spain.strip()
                    russian = russian.strip()

                    if spain.count(',') == 2:
                        irregular_verbs = True
                    else:
                        irregular_verbs = False

                    other_word = Words.objects.filter(
                        russian=russian,
                        lesson__in=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13),
                    )
                    for word in other_word:
                        if word.spain != spain:
                            russian = russian + " (" + str(lesson) + ")"
                    try:
                        Words.objects.get(spain=spain, russian=russian, lesson=lesson)
                    except ObjectDoesNotExist:
                        Words.objects.create(
                            spain=spain,
                            russian=russian,
                            lesson=lesson,
                            irregular_verbs=irregular_verbs,
                        )
                except Exception as ex:
                    print(ex)
        return redirect("spain:settings")

class R_S(View):
    """
    russian to spain translation
    """

    @staticmethod
    def get(request):
        params = WordParamsSpain.objects.get(user=request.user)
        return render(request, "spain/r-s.html", {"params": params})

    @staticmethod
    def post(request):
        params = WordParamsSpain.objects.get(user=request.user)
        context = {"control_state": params.control_state}
        all = WordParamsSpain.get_words(request.user.id)

        for item in all:
            try:
                if item.russian not in context:
                    context[item.russian] = item.spain
            except:
                print("error")
        return JsonResponse(context)


@login_required()
def word_update(request, id):
    """
    crud operations
    :param request:
    :param id:
    :return:
    """
    if request.method == "GET":
        word = Words.objects.get(pk=id)
        context = {"word": word}
        return render(request, "spain/word_form.html", context)
    else:
        spain = request.POST.get("spain")
        russian = request.POST.get("russian")
        info = request.POST.get("info")
        heavy = request.POST.get("heavy")
        learned = request.POST.get("learned")
        lesson = request.POST.get("lesson")
        repeat_learn = request.POST.get("repeat_learn")
        irregular = request.POST.get("irregular")
        important = request.POST.get("important")
        word = Words.objects.get(pk=id)
        word.spain = spain
        word.russian = russian
        word.info = info

        if heavy:
            word.heavy = True
        else:
            word.heavy = False
        if learned:
            word.learned = True
        else:
            word.learned = False
        if irregular:
            word.irregular_verbs = True
        else:
            word.irregular_verbs = False
        if important:
            word.important = True
        else:
            word.important = False
        word.repeat_learn = int(repeat_learn)
        word.lesson = int(lesson)
        word.save()
        return render(request, "spain/back.html")


@login_required()
def word_delete(request, id):
    """
    crud operations
    :param request:
    :param id:
    :return:
    """
    w = Words.objects.get(id=id)
    w.delete()
    return redirect("spain:list_words")
