from django.db import models


class RecipeManager(models.Manager):
    @staticmethod
    def tag_filter(tags):
        from .models import Recipe

        if tags:
            return Recipe.objects.filter(tag__name__in=tags).distinct()
        else:
            return Recipe.objects.all()


class FavoriteRecipeManager(models.Manager):
    @staticmethod
    def favorite_recipe(user, tags):
        from .models import Recipe, FavoriteRecipe

        favorite = FavoriteRecipe.objects.filter(user=user).all()
        recipes_id = favorite.values_list("recipe", flat=True)
        favorite_list = (
            Recipe.objects.tag_filter(tags)
            .filter(pk__in=recipes_id)
            .order_by("-pub_date")
        )
        return favorite_list
