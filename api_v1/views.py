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
        """ Добавление в избранное. """

        recipe_id = json.loads(request.body)["id"]
        if not recipe_id:
            return JsonResponse(
                {"success": "false", "massage": "id not found"}, status=400
            )
        else:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            FavoriteRecipe.objects.get_or_create(
                user=request.user, recipe=recipe
            )
            return JsonResponse({"success": True})

    def delete(self, request, recipe_id):
        """ Удаление из избранного. """

        recipe = get_object_or_404(Recipe, id=recipe_id)
        FavoriteRecipe.objects.filter(
            user=request.user, recipe=recipe
        ).delete()
        return JsonResponse({"success": True})


class Subscribe(View):
    """ Подписки добавить/удалить. """

    def post(self, request):
        """ Подписка на пользователя. """

        author_id = json.loads(request.body)["id"]
        if not author_id:
            return JsonResponse(
                {"success": "false", "massage": "id not found"}, status=400
            )
        else:
            author = get_object_or_404(User, id=author_id)
            Follow.objects.get_or_create(user=request.user, author=author)
            return JsonResponse({"success": True})

    def delete(self, request, author_id):
        """ Отписка от пользователя. """

        author = get_object_or_404(User, id=author_id)
        Follow.objects.filter(user=request.user, author=author).delete()
        return JsonResponse({"success": True})


class Purchases(View):
    """ Список покупок может добавлять/удалять только его владелец. """

    def post(self, request):
        """ Добавление в список покупок. """

        recipe_id = json.loads(request.body)["id"]
        if not recipe_id:
            return JsonResponse(
                {"success": "false", "massage": "id not found"}, status=400
            )
        else:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            Purchase.objects.get_or_create(user=request.user, recipe=recipe)
            return JsonResponse({"success": True})

    def delete(self, request, recipe_id):
        """ Удаление из списка покупок. """

        recipe = get_object_or_404(Recipe, id=recipe_id)
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
