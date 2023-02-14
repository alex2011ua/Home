from django import forms


class UserRegistrationForm(forms.Form):

    user_name = forms.CharField(label="Your name", max_length=100)
    user_mail = forms.EmailField(label="your e-mail", max_length=200)
    user_password = forms.CharField(max_length=32, widget=forms.PasswordInput)
