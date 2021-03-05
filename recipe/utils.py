from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from recipe.models import RecipeIngredient, Ingredient

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


def generate_shop_list(request):
    """ генерирует список покупок для выгрузки """

    # для кого формируется список покупок
    user = get_object_or_404(User, username=request.user.username)
    # рецепты, ингридиенты которого составят список покупок
    recipes = user.purchases.all()
    ingredients = {}

    # Идем циклом по рецептам
    for i in recipes:
        # Получаем все ингридиенты для конкретного рецепта
        recipe = RecipeIngredient.objects.filter(recipe=i.recipe)
        for i in recipe:
            if ingredients.get(i.ingredient.name):
                # Если есть - суммируем ту еденицу в чем он измеряется
                ingredients[i.ingredient.name][0] += i.weight
            else:
                # Если в словаре еще нет этого продукта, добавляем
                ingredients[i.ingredient.name] = [
                    i.weight,
                    i.ingredient.measure,
                ]

    result = []
    # Подготавливаем финальный список
    for k, v in ingredients.items():
        result.append(f"{k}   {v[0]}  {v[1]}")

    return result
