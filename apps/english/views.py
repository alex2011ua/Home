from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from .form import CompareWordForm, LoadWordForm, LoadWordsForm, SearchWordForm, WordsParamForm
from .models import WordParams, Words


@login_required
def index(request):
    """
    Выбор списка слов
    :param request:
    :return:
    """
    if request.method == "GET":
        try:
            params = WordParams.objects.get(user=request.user)
        except:
            params = WordParams.objects.create(user=request.user)
        form_word_param = WordsParamForm(instance=params)
        all = WordParams.get_words(request.user.id)
        return render(
            request,
            "english/base_english.html",
            {"form_word_param": form_word_param, "params": params, "count": len(all)},
        )
    if request.method == "POST":
        params = WordParams.objects.get(user=request.user)
        form = WordsParamForm(request.POST, instance=params)
        if form.is_valid():
            form.save()
        return redirect("english:english_index")


class Settings(LoginRequiredMixin, PermissionRequiredMixin, View):
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
            "english/settings.html",
            {
                "form_word": form_word,
                "form_list_words": form_list_words,
                "count": count,
            },
        )

    @staticmethod
    def post(request):
        if request.POST.get("english"):
            form = LoadWordForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect("english:settings")
        if request.FILES.get("file"):
            name_file, _ = request.FILES.get("file").name.split(".")
            irregular_verbs = False
            phrasal_verbs = False

            try:
                lesson = int(name_file)
            except:
                lesson = 99

            if name_file == "irregular_verbs":
                irregular_verbs = True
            elif name_file == "phrasal_verbs":
                phrasal_verbs = True
            file_ = request.FILES.get("file").read()
            content = file_.decode("utf-8").split("\r\n")
            if len(content) < 2:  # git modify text file and delete \r
                content = file_.decode("utf-8").split("\n")
            for item in content:
                try:
                    item = item.strip()
                    item = item.replace("’", "'")

                    if ";" in item:
                        english, russian = item.split(";", 1)
                    elif "•" in item:
                        english, russian = item.split("•", 1)
                    elif "-" in item:
                        english, russian = item.split("-", 1)
                    if english.startswith("(to)"):
                        english = english.replace("(to)", "to", 1)
                    english = english.strip()
                    russian = russian.strip()

                    if english.count(',') == 2:
                        irregular_verbs = True
                    else:
                        irregular_verbs = False

                    other_word = Words.objects.filter(
                        russian=russian,
                        lesson__in=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13),
                    )
                    for word in other_word:
                        if word.english != english:
                            russian = russian + " (" + str(lesson) + ")"
                    try:
                        Words.objects.get(english=english, russian=russian, lesson=lesson)
                    except ObjectDoesNotExist:
                        Words.objects.create(
                            english=english,
                            russian=russian,
                            lesson=lesson,
                            irregular_verbs=irregular_verbs,
                            phrasal_verbs=phrasal_verbs,
                        )
                except Exception as ex:
                    print(ex)
        return redirect("english:settings")


@login_required()
def clear_control(request):
    """
    clear control lable
    :param request:
    :return:
    """
    params = WordParams.objects.get(user=request.user)
    params.control_state = False
    params.save()
    all = WordParams.get_words(request.user.id)
    all.update(control=False)
    return redirect("english:english_index")


@login_required()
def clear_learned(request):
    """
    clear learned lable
    :param request:
    :return:
    """
    params = WordParams.objects.get(user=request.user)
    params.learned = False
    params.save()
    all = WordParams.get_words(request.user.id)
    all.update(learned=False)
    return redirect("english:english_index")


def test(request):
    """для перехода на следующий уровень. не использовать."""
    # all = Words.objects.all()
    # for i in all:
    #     if i.learned:
    #         i.add_learned(request.user.id)
    #     if i.heavy:
    #         i.add_heavy(request.user.id)
    #     if i.control:
    #         i.add_control(request.user.id)
    #
    # return render(request, "english/back.html")
    words_l4 = Words.objects.filter(lesson__in=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
    for word in words_l4:
        english = word.english
        russian = word.russian
        Words.objects.create(
            english=english,
            russian=russian,
            lesson=400,

            learned=word.learned,
            heavy=word.heavy,
            control=word.control,

            phrasal_verbs=word.phrasal_verbs,
            irregular_verbs=word.irregular_verbs,

            info=str(word.lesson),
            repeat_learn=word.repeat_learn,
            important=word.important,

        )
        word.delete()

    return render(request, "english/back.html")


def list_words(request):
    """
    list checking words
    :param request:
    :return:
    """
    if request.method == "GET":
        all = WordParams.get_words(request.user.id)
        return render(request, "english/list_words.html", {"words": all, "count": len(all)})


@login_required()
@permission_required("is_staff")
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
        return render(request, "english/word_form.html", context)
    else:
        english = request.POST.get("english")
        russian = request.POST.get("russian")
        info = request.POST.get("info")
        heavy = request.POST.get("heavy")
        learned = request.POST.get("learned")
        lesson = request.POST.get("lesson")
        repeat_learn = request.POST.get("repeat_learn")
        phrasal = request.POST.get("phrasal")
        irregular = request.POST.get("irregular")
        important = request.POST.get("important")
        word = Words.objects.get(pk=id)
        word.english = english
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
        if phrasal:
            word.phrasal_verbs = True
        else:
            word.phrasal_verbs = False
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
        return render(request, "english/back.html")


@login_required()
@permission_required("is_staff")
def word_delete(request, id):
    """
    crud operations
    :param request:
    :param id:
    :return:
    """
    w = Words.objects.get(id=id)
    w.delete()
    return redirect("english:list_words")


class E_R(View):
    """
    english to russian translation
    """

    @staticmethod
    def get(request):
        params = WordParams.objects.get(user=request.user)
        return render(request, "english/e-r.html", {"params": params})

    @staticmethod
    def post(request):
        all = WordParams.get_words(request.user.id)
        params = WordParams.objects.get(user=request.user)
        context = {"control_state": params.control_state}
        for item in all:
            try:
                context[item.english] = item.russian
            except Exception:
                print("error")
        return JsonResponse(context)


class R_E(View):
    """
    russian to english translation
    """

    @staticmethod
    def get(request):
        params = WordParams.objects.get(user=request.user)
        return render(request, "english/r-e.html", {"params": params})

    @staticmethod
    def post(request):
        params = WordParams.objects.get(user=request.user)
        context = {"control_state": params.control_state}
        all = WordParams.get_words(request.user.id)

        for item in all:
            try:
                if item.russian not in context:
                    context[item.russian] = item.english
            except:
                print("error")
        return JsonResponse(context)


@login_required()
def mod(request):
    """
    change lables
    :param request:
    :return:
    """

    def mod_db(mod, word):
        s = Words.objects.filter(**word)
        for w in s:
            if mod == "learned":
                w.add_learned(request.user.id)
            elif mod == "heavy":
                w.add_heavy(request.user.id)
            elif mod == "not_heavy":
                w.dell_heavy(request.user.id)
            elif mod == "control":
                w.add_control(request.user.id)

    p = WordParams.params(request.user.id)
    word = {"lesson__in": p["lesson__in"]}
    if "/e_r/" in request.path:
        language = "english"
    else:
        language = "russian"
    print(request.GET)
    if request.GET.get("learned"):
        mod = "learned"
        word[language] = request.GET.get("learned")
        mod_db(mod, word)
    if request.GET.get("heavy"):
        mod = "heavy"
        word[language] = request.GET.get("heavy")
        mod_db(mod, word)
    if request.GET.get("not_heavy"):
        mod = "not_heavy"
        word[language] = request.GET.get("not_heavy")
        mod_db(mod, word)
    if request.GET.get("control"):
        mod = "control"
        word[language] = request.GET.get("control")
        mod_db(mod, word)

    context = {"status": 200}
    return JsonResponse(context)


class SearchWord(View):
    """
    search words in my bd
    """

    @staticmethod
    def get(request):
        form = SearchWordForm()
        return render(request, "english/search_word.html", {"form": form})

    @staticmethod
    def post(request):
        form = SearchWordForm()
        input_word = request.POST.get("word")
        english_words = Words.objects.filter(english__icontains=input_word)
        russian_words = Words.objects.filter(russian__icontains=input_word)

        count = len(english_words) + len(russian_words)

        return render(
            request,
            "english/search_word.html",
            {
                "form": form,
                "english_words": english_words,
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
        return render(request, "english/compare_word.html", {"form": form})

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
            "english/compare_word.html",
            {
                "form": form,
                "answer": answer,
                "first_word": first_word,
                "second_word": second_word,
            },
        )


class Repeat(View):
    """
    Repeat all learned words
    """

    @staticmethod
    def get(request):
        count_all = Words.objects.all().count() - 183  # count game words
        count_learn = Words.objects.filter(important=True).count() - 183
        count_5 = Words.objects.filter(important=False, repeat_learn__gt=4).count()
        count_4 = Words.objects.filter(important=False, repeat_learn=4).count()
        count_3 = Words.objects.filter(important=False, repeat_learn=3).count()
        count_2 = Words.objects.filter(important=False, repeat_learn=2).count()
        count_1 = Words.objects.filter(important=False, repeat_learn=1).count()

        return render(request, "english/repeat.html", {
            "count": 20,
            "count_all": count_all,
            "count_learn": count_learn,
            "count_5": count_5,
            "count_4": count_4,
            "count_3": count_3,
            "count_2": count_2,
            "count_1": count_1,
        })
