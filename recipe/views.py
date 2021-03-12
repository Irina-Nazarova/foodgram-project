from django.contrib.auth.decorators import login_required
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
    FavoriteRecipe,
)
from recipe.utils import generate_shop_list, pagination


def index(request):
    """Отображение главной страницы."""

    active_index = True
    tags = request.GET.getlist("filters")
    recipe_types = Recipe.objects.tag_filter(tags)
    paginator, page = pagination(request, recipe_types, OBJECT_PER_PAGE)
    context = {
        "page": page,
        "paginator": paginator,
        "active_index": active_index,
    }
    return render(request, "recipe/index.html", context)


@login_required
def recipe_create(request):
    """ Cоздание нового рецепта. """

    active_create = True
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        initial={"request": request},
    )

    if form.is_valid():
        form.save()
        return redirect("index")

    context = {
        "name": "name",
        "form": form,
        "description": "description",
        "cook_time": "cook_time",
        "picture": "picture",
        "active_create": active_create,
    }
    return render(request, "recipe/recipe_action.html", context)


@login_required
def recipe_edit(request, recipe_id):
    """Cтраница редактирования рецепта."""

    recipe = get_object_or_404(Recipe, id=recipe_id)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe,
        initial={"request": request},
    )

    if form.is_valid():
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        form.save()
        return redirect("index")

    return render(
        request, "recipe/recipe_action.html", {"form": form, "recipe": recipe}
    )


@login_required
def recipe_delete(request, recipe_id):
    """Удаление рецепта."""

    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
    return redirect("index")


def recipe_view(request, username, recipe_id):
    """Страница просмотра рецепта."""

    recipe = get_object_or_404(Recipe, id=recipe_id)
    author = get_object_or_404(User, username=username)
    following = False
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user, author=author
        ).exists()
    return render(
        request,
        "recipe/recipe_view.html",
        {
            "recipe": recipe,
            "following": following,
        },
    )


@login_required
def favorite_recipes(request, username):
    """Страница избранных рецептов."""

    active_favorites = True
    tag_value = request.GET.getlist("filters")
    favorite_list = FavoriteRecipe.objects.favorite_recipe(
        request.user, tag_value
    )
    paginator, page = pagination(request, favorite_list, OBJECT_PER_PAGE)
    context = {
        "page": page,
        "paginator": paginator,
        "active_favorites": active_favorites,
    }
    return render(request, "recipe/favorite.html", context)


@login_required
def profile(request, username):
    """Страница автора рецептов."""

    author = get_object_or_404(User, username=username)
    tag_value = request.GET.getlist("filters")
    recipe_tags = Recipe.objects.tag_filter(tag_value).filter(author=author)
    following = False
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user, author=author
        ).exists()

    paginator, page = pagination(request, recipe_tags, OBJECT_PER_PAGE)
    return render(
        request,
        "recipe/author_profile.html",
        {
            "page": page,
            "paginator": paginator,
            "following": following,
            "author": author,
        },
    )


@login_required
def follow_index(request, username):
    """Страница мои подписки."""

    active_follow = True
    user_follow = get_object_or_404(User, username=username)
    authors = Follow.objects.filter(user=user_follow)
    paginator, page = pagination(request, authors, OBJECT_PER_PAGE)
    return render(
        request,
        "recipe/my_follow.html",
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
    """Страница списка покупок."""

    active_purchases = True
    purchases = Purchase.objects.filter(user=request.user)
    return render(
        request,
        "recipe/shop_list.html",
        {"purchases": purchases, "active_purchases": active_purchases},
    )


@login_required
def purchases_delete(request, recipe_id):
    """Удаление рецепта из списка покупок."""

    recipe = get_object_or_404(Recipe, id=recipe_id)
    Purchase.objects.filter(user=request.user, recipe=recipe).delete()
    return redirect("recipes:purchases_index")


@login_required
def download(request):
    """Скачать список покупок в PDF файл."""

    result = generate_shop_list(request)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="purchases.pdf"'
    p = canvas.Canvas(response)
    top_line = 810
    p.drawString(10, top_line, "Purchases:")

    for i in result:
        top_line -= 20
        p.drawString(10, top_line, i)
    p.showPage()
    p.save()
    return response
