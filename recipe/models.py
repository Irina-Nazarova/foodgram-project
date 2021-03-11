from django.db import models
from django.contrib.auth import get_user_model

from .managers import RecipeManager, FavoriteRecipeManager

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=5000, verbose_name="ingredient's name", unique=True
    )
    measure = models.CharField(max_length=100, verbose_name="measurement unit")

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tag(models.Model):
    value = models.CharField("Value", max_length=10, unique=True)
    name = models.CharField("Visible name", max_length=25, unique=True)
    color = models.CharField("Color", max_length=10)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200, verbose_name="recipe's name")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes"
    )
    tag = models.ManyToManyField(
        Tag, through="RecipeTag", related_name="recipes"
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        through_fields=("recipe", "ingredient"),
        verbose_name="ingredients",
    )
    description = models.TextField()
    pub_date = models.DateTimeField(
        auto_now=True, db_index=True, verbose_name="publishing date"
    )
    cook_time = models.PositiveSmallIntegerField(
        verbose_name="cook time",
        null=False,
        default=10,
        help_text="Add cook time in minutes",
    )
    picture = models.ImageField(
        upload_to="recipe/", verbose_name="picture of the recipe"
    )
    objects = RecipeManager()

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"
        ordering = ["-pub_date"]

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipe_ingredients"
    )

    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.PROTECT, related_name="recipe_ingredients"
    )

    weight = models.PositiveSmallIntegerField(
        verbose_name="weight_ingredients",
        null=False,
        default=10,
        help_text="Add needed weight for the recipe",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"], name="recipe_unique"
            )
        ]
        verbose_name = "Recipe Ingredient"
        verbose_name_plural = "Recipes Ingredients"
        ordering = ["recipe"]

    def __str__(self):
        return self.ingredient.name


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Recipe title",
        related_name="recipe_tags",
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name="Tag name",
        related_name="recipe_tags",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "tag"], name="recipe_tag_unique"
            )
        ]
        verbose_name = "Recipe tags"
        verbose_name_plural = "Recipe tags"


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="liker"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favorite_recipes"
    )
    objects = FavoriteRecipeManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="favorite_unique"
            )
        ]
        verbose_name = "Favorite Recipe"
        verbose_name_plural = "Favorite Recipes"
        ordering = ["user"]

    def __str__(self):
        return f"favorite recipe - {self.recipe.name}"


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"], name="follow_unique"
            )
        ]
        ordering = [
            "-id",
        ]


class Purchase(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="purchases"
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="purchase_unique"
            )
        ]
        verbose_name = "Shopping List"
        verbose_name_plural = "Shopping Lists"
        ordering = ["recipe"]
