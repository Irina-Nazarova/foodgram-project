from .models import Purchase


def counter(request):
    """ счетчик для списка покупок в заголовке  """

    if request.user.is_authenticated:
        count = Purchase.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'count': count}
