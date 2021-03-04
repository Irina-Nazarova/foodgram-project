from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()


def get_ingredients(request):
    """генерирует список ингредиентов при создании/редактировании рецепта,
    достает из POST запроса"""

    ingredients = {}  # словарь для списка ингредиентов

    for key in request.POST:
        if key.startswith("nameIngredient"):
            value_ingredient = key[15:]  # получаем количество
            ingredients[request.POST[key]] = request.POST[
                "valueIngredient_" + value_ingredient
            ]

    return ingredients
