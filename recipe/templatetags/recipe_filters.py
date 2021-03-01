from django import template

from recipe.models import FavoriteRecipe, Purchase

register = template.Library()


@register.filter()
def is_favorite(recipe, user):
    """ фильтр проверки находится ли рецепт в избранном """
    return FavoriteRecipe.objects.filter(user=user, recipe=recipe).exists()


@register.filter()
def url_with_get(request, number):
    query = request.GET.copy()
    query['page'] = number
    return query.urlencode()


@register.filter
def subtract(value, arg):
    return value - arg

@register.filter(name='is_purchase')
def is_purchase(recipe, user):
    """ фильтр проверки находится ли рецепт в списке покупок """
    return Purchase.objects.filter(user=user, recipe=recipe).exists()



