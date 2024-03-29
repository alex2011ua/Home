from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponse
from apps.english.models import WordParams
from django.core.mail import send_mail
from AlexUA_Home import settings
from AlexUA_Home.registration_form import UserRegistrationForm


class EmailFormSabmit(View):
    @staticmethod
    def post(request, *args, **kwargs):
        print(request.POST)
        send_mail(
            subject="Someone write me from my site",
            message=f"Name: {request.POST.get('name')}, email: {request.POST.get('email'),}, subject: {request.POST.get('subject')}, message: {request.POST.get('message')}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["alex2011ua@gmail.com"],
        )
        return HttpResponse("OK", status=200)


class IndexView(View):
    @staticmethod
    def get(request):
        context = {"inline": "none"}
        return render(request, "start/index.html", context=context)


class Portfolio(View):
    @staticmethod
    def get(request, job):
        return render(request, f"start/portfolio_{job}.html")


    @staticmethod
    def post(request):
        print(request.POST)
        return render(request, "start/index.html", context={"inline": ""})


class RegisterView(View):
    @staticmethod
    def get(request):
        form = UserRegistrationForm()
        return render(request, "registration/registration.html", {"form": form})

    @staticmethod
    def post(request):
        user_name = request.POST.get("user_name")
        user_password = request.POST.get("user_password")
        user_mail = request.POST.get("user_mail")
        # Создайте пользователя и сохраните его в базе данных
        user = User.objects.create_user(user_name, user_mail, user_password)
        WordParams.objects.create(user=user)

        return redirect("login")
