import json

from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View


from recipe.models import (
    Recipe,
    FavoriteRecipe,
    Follow,
    User,
    Purchase,
    Ingredient,
)


class Favorite(View):
    """ При необходимости пользователь может добавить/удалить рецепт из избранного. """

    def post(self, request):
        """ Добавление в избранное. """

        json_data = json.loads(request.body.decode())
        recipe_id = json_data.get("id")

        if recipe_id:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            FavoriteRecipe.objects.get_or_create(
                user=request.user, recipe=recipe
            )
            return JsonResponse({"success": True})
        else:
            return JsonResponse(
                {"success": "false", "message": "id not found"}, status=400
            )

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

        json_data = json.loads(request.body.decode())
        author_id = json_data.get("id")

        if author_id:
            author = get_object_or_404(User, id=author_id)
            Follow.objects.get_or_create(user=request.user, author=author)
            return JsonResponse({"success": True})
        else:
            return JsonResponse(
                {"success": "false", "message": "id not found"}, status=400
            )

    def delete(self, request, author_id):
        """ Отписка от пользователя. """

        author = get_object_or_404(User, id=author_id)
        Follow.objects.filter(user=request.user, author=author).delete()
        return JsonResponse({"success": True})


class ShopingList(View):
    """ Список покупок может добавлять/удалять только его владелец. """

    def post(self, request):
        """ Добавление в список покупок. """

        json_data = json.loads(request.body.decode())
        recipe_id = json_data.get("id")
        if recipe_id:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            Purchase.objects.get_or_create(user=request.user, recipe=recipe)
            return JsonResponse({"success": True})
        else:
            return JsonResponse(
                {"success": "false", "message": "id not found"}, status=400
            )

    def delete(self, request, recipe_id):
        """ Удаление из списка покупок. """

        recipe = get_object_or_404(Recipe, id=recipe_id)
        Purchase.objects.filter(user=request.user, recipe=recipe).delete()
        return JsonResponse({"success": True})


class AddIngredient(View):
    """ Для автозаполнения поля ингредиентов в форме создания/редактирования рецепта. """

    def get(self, request):
        text = request.GET.get("query")
        ingredients = list(
            Ingredient.objects.filter(name__startswith=text).values(
                title=F("name"), dimension=F("measure")
            )
        )
        return JsonResponse(ingredients, safe=False)
