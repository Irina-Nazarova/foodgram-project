from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("recipes:index")
    template_name = "registration/signup.html"



# позволяет узнать ссылку на URL по его имени, параметр name функции path
# from django.urls import reverse_lazy
# from django.views.generic import CreateView

# from users.forms import CreationForm
#
#
# class SignUpView(CreateView):
#     form_class = CreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'user/signup.html'

