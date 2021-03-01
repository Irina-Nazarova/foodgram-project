from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from foodgram.settings import OBJECT_PER_PAGE
from recipe.forms import RecipeForm
from recipe.models import User, Recipe, Follow, Purchase
from recipe.utils import generate_shop_list


def index(request):
    """ главная страница """

    active_index = True  # для подсвечивания активного раздела

    all_recipes = Recipe.objects.all()
    paginator = Paginator(all_recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {"page": page,
               "paginator": paginator,
               "all_recipes": all_recipes,
               "active_index": active_index,}
    return render(request, "index.html", context)


def recipe_create(request):
    """ создание рецепта """

    active_recipe_create = True  # для подсвечивания активного раздела

    if request.method == 'POST':
        # TODO: Добавить ингридиенты, тип (Завтрак, обед, ужин)
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            f = form.save(commit=False)
            f.author = request.user
            f.save()
            return redirect("index")
        else:
            error = "рецепт не добавлен, ошибка валидации формы"     # дебаг, удалить в HTML после
            return render(request, "recipe_create.html", {"error": error})
    else:
        form = RecipeForm()
        context = {
            "name": "name",
            "form": form,
            "description": "description",
            "cook_time": "cook_time",
            "picture": "picture",
            "active_recipe_create": active_recipe_create,
        }
        return render(request, "recipe_create.html", context)


def recipe_view(request, username, recipe_id):
    """ страница просмотра рецепта """

    recipe = get_object_or_404(Recipe, id=recipe_id)  # рецепт который нужно отразить
    author = get_object_or_404(User, username=username)  # автор рецепта

    # проверяем, подписан ли текущий пользователь на автора
    following = False
    if request.user.is_authenticated:
        following = Follow.objects.filter(user=request.user, author=author).exists()
    return render(request, 'recipe_view.html', {'recipe': recipe, 'following': following})


def favorite_recipes(request, username):
    """ страница избранных рецептов """

    all_recipes = Recipe.objects.filter(favorite__user__id=request.user.id)
    paginator = Paginator(all_recipes, OBJECT_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {"page": page,
               "paginator": paginator,
               "all_recipes": all_recipes}
    return render(request, "favorite.html", context)


def profile(request, username):
    """ страница автора рецептов """

    author = get_object_or_404(User, username=username)  # автор, чья страница
    recipes = Recipe.objects.filter(author=author)
    following = False  # на кого подписались
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user, author=author).exists()

    paginator = Paginator(recipes, OBJECT_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'author_profile.html', {
        'page': page,
        'paginator': paginator,
        'following': following,
        'author': author},)


def follow_index(request, username):
    """страница Мои подписки"""

    user_follow = get_object_or_404(User, username=username)  # кто подписывается
    # авторы, на которых подписан
    authors = Follow.objects.filter(user=user_follow)
    active_follow = True  # для подсвечивания активного раздела

    paginator = Paginator(authors, OBJECT_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'my_follow.html', {
        'page': page,
        'paginator': paginator,
        'user_follow': user_follow,
        'active_follow': active_follow,
        'authors': authors},)


def purchases_index(request):
    """страница списка покупок"""

    purchases = Purchase.objects.filter(user=request.user)

    return render(request, 'shop_list.html', {'purchases': purchases},)


def purchases_delete(request, recipe_id):
    """ удаление рецепта из списка покупок """

    # получаем рецепт, который хотим удалить
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # удаляем рецепт из списка
    Purchase.objects.filter(user=request.user, recipe=recipe).delete()

    return redirect('recipes:purchases_index')


def download(request):
    """скачивание списка покупок"""
    # функция, формирующая список покупок
    result = generate_shop_list(request)  # utils
    filename = 'shop_list.txt'
    response = HttpResponse(result, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response


# def page_not_found(request, exception):
#     #  переменная exception содержит отладочную информацию,
#     #  выводить её в шаблон пользовательской страницы 404 не нужно
#     return render(request, 'misc/404.html', {'path': request.path}, status=404)
#
#
# def server_error(request):
#     return render(request, 'misc/500.html', status=500)

