from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from recipe.models import RecipeIngredient, Ingredient

User = get_user_model()


def get_ingredients(request):
    """
    Генерирует список ингредиентов при создании/редактировании рецепта,
    достает из POST запроса.
    """

    ingredients = {}

    for key in request.POST:
        if key.startswith("nameIngredient"):
            value_ingredient = key[15:]
            ingredients[request.POST[key]] = request.POST[
                "valueIngredient_" + value_ingredient
            ]

    return ingredients


def generate_shop_list(request):
    """ Генерирует список покупок для выгрузки. """

    user = get_object_or_404(User, username=request.user.username)
    purchases = user.purchases.all()
    ingredients = {}

    for purchase in purchases:
        recipe_ingredients = RecipeIngredient.objects.filter(
            recipe=purchase.recipe
        )

        for item in recipe_ingredients:
            if ingredients.get(item.ingredient.name):
                ingredients[item.ingredient.name][0] += item.weight
            else:
                ingredients[item.ingredient.name] = [
                    item.weight,
                    item.ingredient.measure,
                ]

    result = []
    for k, v in ingredients.items():
        result.append(f"{k}   {v[0]}  {v[1]}")

    return result
