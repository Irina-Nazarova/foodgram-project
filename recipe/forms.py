from django import forms
from django.shortcuts import get_object_or_404

from .models import Recipe, RecipeIngredient
from recipe.models import Ingredient
from recipe.utils import get_ingredients


class RecipeForm(forms.ModelForm):
    picture = forms.ImageField(required=True, label="Add an image")

    def save(self, commit=True):
        request = self.initial["request"]
        recipe = super().save(commit=False)
        recipe.author = request.user
        recipe.save()

        ingredients = get_ingredients(request)
        for item in ingredients:
            RecipeIngredient.objects.create(
                weight=ingredients[item],
                recipe=recipe,
                ingredient=get_object_or_404(Ingredient, name=item),
            )
        self.save_m2m()
        return recipe

    class Meta:
        model = Recipe
        fields = (
            "name",
            "description",
            "cook_time",
            "picture",
            "tag",
        )

        labels = {
            "name": "Recipe title",
            "cook_time": "Total cooking time",
            "description": "Description",
            "picture": "Add an image",
        }
