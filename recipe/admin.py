from django.contrib import admin

from .models import (Ingredient,
                     Recipe,
                     RecipeIngredient,
                     RecipeType,
                     FavoriteRecipe,
                     Follow,
                     Purchase, )


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measure',)
    search_fields = ('name', 'measure',)
    list_filter = ('name', 'measure',)
    empty_value_display = '-empty-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'pub_date',)
    list_display_links = ('name',)
    search_fields = ('name', 'pub_date',)
    empty_value_display = '-empty-'


class RecipeTypeAdmin(admin.ModelAdmin):
    list_display = ('color', 'type_name',)
    search_fields = ('color', 'type_name',)
    list_filter = ('color', 'type_name',)
    empty_value_display = '-empty-'


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'weight',)
    search_fields = ('recipe', 'ingredient',)
    list_filter = ('recipe', 'ingredient',)
    empty_value_display = '-empty-'


class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    empty_value_display = '-empty-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    search_fields = ('user', 'author',)
    list_filter = ('user', 'author',)
    empty_value_display = '-empty-'


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    empty_value_display = '-empty-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeType, RecipeTypeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Purchase, PurchaseAdmin)





