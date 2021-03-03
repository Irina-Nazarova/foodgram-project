from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):
    first_name = forms.CharField(label="Name")
    username = forms.CharField(label="Username")
    email = forms.EmailField(label="Email")
    password2 = None
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")

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

