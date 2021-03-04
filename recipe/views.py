from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from reportlab.pdfgen import canvas

from foodgram.settings import OBJECT_PER_PAGE
from recipe.forms import RecipeForm
from recipe.models import (
    User,
    Recipe,
    Follow,
    Purchase,
    RecipeIngredient,
    RecipeType,
)


def index(request):
    """ главная страница """

    active_index = True  # для подсвечивания активного раздела
    # получаем все теги из БД
    recipe_types = RecipeType.objects.all()

    tag_value = request.GET.getlist("filters")
    if tag_value:
        recipes = Recipe.objects.filter(
            type__type_name__in=tag_value
        ).distinct()
    else:
        recipes = Recipe.objects.all()

    paginator = Paginator(recipes, OBJECT_PER_PAGE)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "paginator": paginator,
        "active_index": active_index,
        "recipe_types": recipe_types,
    }
    return render(request, "index.html", context)


@login_required
def recipe_create(request):
    """ создание рецепта """

    active_create = True  # для подсвечивания активного раздела

    if request.method == "POST":
        # TODO: Добавить ингридиенты, тип (Завтрак, обед, ужин)
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            f = form.save(commit=False)
            f.author = request.user
            f.save()
            # сохраняем данные для полей м2м (тэги и ингредиенты)
            form.save_m2m()
            return redirect("index")
    else:
        form = RecipeForm()
        context = {
            "name": "name",
            "form": form,
            "description": "description",
            "cook_time": "cook_time",
            "picture": "picture",
            "active_create": active_create,
        }
        return render(request, "recipe_create.html", context)


def recipe_edit(request, recipe_id):
    """страница редактирования рецепта"""

    # получаем рецепт по ID
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == "POST":
        form = RecipeForm(
            request.POST or None, files=request.FILES or None, instance=recipe
        )
        # функция, передающая список ингредиентов
        # ingredients = get_ingredients(request)

        # if not ingredients:
        #     form.add_error(None, 'Add at least one ingredient')
        if form.is_valid():
            # удаляем ингредиенты, связанные с рецептом
            RecipeIngredient.objects.filter(recipe=recipe).delete()
            # сохраняем форму, но не отправляем в БД
            recipe = form.save(commit=False)
            recipe.author = request.user  # получаем автора рецепта
            recipe.save()  # сохраняем изменения

            # сохраняем данные для полей м2м (тэги и ингредиенты)
            form.save_m2m()
            return redirect("index")

    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe
    )

    return render(
        request, "edit_recipe.html", {"form": form, "recipe": recipe}
    )


def recipe_delete(request, recipe_id):
    """удаление рецепта"""

    # получаем рецепт по ID
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # если пользователь является автором рецепта, то удаляем рецепт
    if request.user == recipe.author:
        recipe.delete()

    return redirect("index")


def recipe_view(request, username, recipe_id):
    """ страница просмотра рецепта """

    recipe = get_object_or_404(
        Recipe, id=recipe_id
    )  # рецепт который нужно отразить
    author = get_object_or_404(User, username=username)  # автор рецепта

    # проверяем, подписан ли текущий пользователь на автора
    following = False
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user, author=author
        ).exists()
    return render(
        request, "recipe_view.html", {"recipe": recipe, "following": following}
    )


@login_required
def favorite_recipes(request, username):
    """ страница избранных рецептов """

    active_favorites = True

    recipe_types = RecipeType.objects.all()

    tag_value = request.GET.getlist("filters")
    if tag_value:
        recipes = Recipe.objects.filter(
            type__type_name__in=tag_value, favorite__user__id=request.user.id
        ).distinct()
    else:
        recipes = Recipe.objects.filter(favorite__user__id=request.user.id)

    paginator = Paginator(recipes, OBJECT_PER_PAGE)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "paginator": paginator,
        "recipe_types": recipe_types,
        "active_favorites": active_favorites,
    }
    return render(request, "index.html", context)


def profile(request, username):
    """ страница автора рецептов """

    author = get_object_or_404(User, username=username)  # автор, чья страница
    recipes = Recipe.objects.filter(author=author)
    following = False  # на кого подписались
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user, author=author
        ).exists()

    paginator = Paginator(recipes, OBJECT_PER_PAGE)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(
        request,
        "index.html",
        {
            "page": page,
            "paginator": paginator,
            "following": following,
            "author": author,
        },
    )


@login_required
def follow_index(request, username):
    """страница мои подписки"""

    active_follow = True  # для подсвечивания активного раздела

    user_follow = get_object_or_404(
        User, username=username
    )  # кто подписывается
    # авторы, на которых подписан пользователь
    authors = Follow.objects.filter(user=user_follow)

    paginator = Paginator(authors, OBJECT_PER_PAGE)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(
        request,
        "my_follow.html",
        {
            "page": page,
            "paginator": paginator,
            "user_follow": user_follow,
            "active_follow": active_follow,
            "authors": authors,
        },
    )


@login_required
def purchases_index(request):
    """страница списка покупок"""

    active_purchases = True  # для подсвечивания активного раздела

    purchases = Purchase.objects.filter(user=request.user)

    return render(
        request,
        "shop_list.html",
        {"purchases": purchases, "active_purchases": active_purchases},
    )


def purchases_delete(request, recipe_id):
    """ удаление рецепта из списка покупок """

    # получаем рецепт, который хотим удалить
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # удаляем рецепт из списка
    Purchase.objects.filter(user=request.user, recipe=recipe).delete()

    return redirect("recipes:purchases_index")


@login_required
def download(request):
    """ Скачать список покупок в PDF файл """

    # Создаем HttpResponse объект соответствующием заголовком
    # application/pdf - говорим браузеру, что загрузится pdf, а не html страница
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="purchases.pdf"'
    # Создаем PDF объект, используя объект ответа как файл
    p = canvas.Canvas(response)
    # Отступ от нижнего края документа
    top_line = 810
    # Заголовок
    p.drawString(10, top_line, "Purchases:")
    # В цикле добавляем каждую строчку к покупке
    for i in range(0, 5):
        # -20 - отступ от предыдущей строки
        top_line -= 20
        # TODO: Сейчас не реализована модель Ingredients, тем самым доставить список не откуда.
        p.drawString(10, top_line, f"{i}. Rcipe {i}")
    p.showPage()
    p.save()
    return response


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
