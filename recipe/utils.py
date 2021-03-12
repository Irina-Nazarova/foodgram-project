from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from recipe.models import RecipeIngredient

User = get_user_model()


def pagination(request, data, count_item):
    """Метод формирующий пагинацию."""

    paginator = Paginator(data, count_item)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return paginator, page


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
    for ingredient, measure in ingredients.items():
        result.append(f"{ingredient}   {measure[0]}  {measure[1]}")

    return result


def is_positive_weight(request):
    """ Проверяем что значение в ингридиентах больше >= 0 """
    result = True
    for i in request.POST.keys():
        if i.startswith('valueIngredient') and int(request.POST[i]) < 0:
            result = False
            break
    return result
