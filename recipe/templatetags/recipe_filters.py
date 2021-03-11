from django import template

from recipe.models import FavoriteRecipe, Purchase, Tag, RecipeTag

register = template.Library()


@register.filter()
def is_favorite(recipe, user):
    """Фильтр проверки находится ли рецепт в избранном."""
    return FavoriteRecipe.objects.filter(user=user, recipe=recipe).exists()


@register.filter()
def url_with_get(request, number):
    query = request.GET.copy()
    query["page"] = number
    return query.urlencode()


@register.filter()
def subtract(value, arg):
    return value - arg


@register.filter()
def is_purchase(recipe, user):
    """Фильтр проверки находится ли рецепт в списке покупок."""
    return Purchase.objects.filter(user=user, recipe=recipe).exists()


@register.filter(name="get_filter_link")
def get_filter_link(request, tag):
    new_request = request.GET.copy()

    if tag.name in request.GET.getlist("filters"):
        filters = new_request.getlist("filters")
        filters.remove(tag.name)
        new_request.setlist("filters", filters)
    else:
        new_request.appendlist("filters", tag.name)

    return new_request.urlencode()


@register.filter(name="get_filter_values")
def get_filter_values(value):
    return value.getlist("filters")


@register.filter()
def all_tags(value):
    return Tag.objects.all()


@register.filter()
def is_in_type(tag, recipe):
    type_exists = RecipeTag.objects.filter(tag=tag, recipe=recipe).exists()
    return type_exists
