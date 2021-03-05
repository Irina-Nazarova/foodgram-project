import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.db.models import F
from recipe.models import (
    Recipe,
    FavoriteRecipe,
    Follow,
    User,
    Purchase,
    Ingredient,
)


class Favorites(View):
    """ При необходимости пользователь может добавить/удалить рецепт из избранного. """

    def post(self, request):
        """ добавление в избранное """
        # получаем id рецепта, которого хотим добавить в избранное
        recipe_id = json.loads(request.body)["id"]
        # получаем рецепт, который хотим добавить в избранное
        recipe = get_object_or_404(Recipe, id=recipe_id)

        FavoriteRecipe.objects.get_or_create(user=request.user, recipe=recipe)
        return JsonResponse({"success": True})

    def delete(self, request, recipe_id):
        """ Удаление из избранного. """

        # находим рецепт, который хотим удалить
        recipe = get_object_or_404(Recipe, id=recipe_id)
        # удаляем рецепт из избранного текущего пользователя
        FavoriteRecipe.objects.filter(
            user=request.user, recipe=recipe
        ).delete()
        return JsonResponse({"success": True})


class Subscribe(View):
    """ Подписки добавить/удалить. """

    def post(self, request):
        """ Подписка на пользователя. """

        # получаем id пользователя, на которого хотим подписаться
        author_id = json.loads(request.body)["id"]
        # получаем пользователя, на которого хотим подписаться
        author = get_object_or_404(User, id=author_id)
        Follow.objects.get_or_create(user=request.user, author=author)
        return JsonResponse({"success": True})

    def delete(self, request, author_id):
        """ Отписка от пользователя. """

        # находим пользователя, от которого хотим отписаться
        author = get_object_or_404(User, id=author_id)
        # удаляем из подписок фолловера пользователя,
        # от которого хотим отписаться
        Follow.objects.filter(user=request.user, author=author).delete()
        return JsonResponse({"success": True})


class Purchases(View):
    """ Список покупок может добавлять/удалять только его владелец. """

    def post(self, request):
        """ Добавление в список покупок. """

        # получаем id рецепта,
        # ингредиенты которого хотим добавить в список покупок
        recipe_id = json.loads(request.body)["id"]
        # получаем рецепт, ингредиенты которого хотим добавить в список покупок
        recipe = get_object_or_404(Recipe, id=recipe_id)
        Purchase.objects.get_or_create(user=request.user, recipe=recipe)
        return JsonResponse({"success": True})

    def delete(self, request, recipe_id):
        """ Удаление из списка покупок. """

        # находим рецепт, который хотим удалить из списка покупок
        recipe = get_object_or_404(Recipe, id=recipe_id)
        # удаляем искомый рецепт из списка текущего пользователя
        Purchase.objects.filter(user=request.user, recipe=recipe).delete()
        return JsonResponse({"success": True})


class Ingredients(View):
    """ Для автозаполнения поля ингредиентов в форме создания/редактирования рецепта. """

    def get(self, request):
        text = request.GET.get("query")
        ingredients = list(
            Ingredient.objects.filter(name__startswith=text).values(
                title=F("name"), dimension=F("measure")
            )
        )
        return JsonResponse(ingredients, safe=False)
