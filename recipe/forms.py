from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    picture = forms.ImageField(
        required=True,
        label='Add an image'
    )

    class Meta:
        model = Recipe
        fields = (
            'name', 'description', 'cook_time', 'picture', 'type',
        )

        labels = {
            'name': 'Recipe title',
            'cook_time': 'Total cooking time',
            'description': 'Description',
            'picture': 'Add an image',
        }
