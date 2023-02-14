from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View

# from apps.english.models import WordParams


from .registration_form import UserRegistrationForm


class IndexView(View):
    @staticmethod
    def get(request):
        context = {
            "s_yers": [2016],
            "po_yers": [2018],
            "price_ot": 10000,
            "price_do": 10500,
            "type": ["1", "4", "6"],
            "gearbox": ["2", "3"],
        }
        return render(request, "start/index.html", context)


class RegisterView(View):
    @staticmethod
    def get(request):
        form = UserRegistrationForm()
        return render(request, "registration/registration.html", {"form": form})

    # @staticmethod
    # def post(request):
    #     user_name = request.POST.get("user_name")
    #     user_password = request.POST.get("user_password")
    #     user_mail = request.POST.get("user_mail")
    #     # Создайте пользователя и сохраните его в базе данных
    #     user = User.objects.create_user(user_name, user_mail, user_password)
    #     WordParams.objects.create(user=user)
    #
    #     return redirect("login")
