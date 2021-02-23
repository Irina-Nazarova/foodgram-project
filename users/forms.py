from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):
    first_name = forms.CharField(label="Имя")
    username = forms.CharField(label="Логин")
    email = forms.EmailField(label="Электронная почта")
    password2 = None
    password1 = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    class Meta:
        model = User
        fields = ("first_name", "username", "email")





# from django import forms
# from django.contrib.auth.forms import UserCreationForm

# from .models import User
#
#
# class CreationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ('first_name', 'last_name', 'username', 'email')

