from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"
        ordering = ["name"]

    name = models.CharField(
        max_length=5000,
        verbose_name="ingredient's name",
        unique=True
    )
    measure = models.CharField(
        max_length=100,
        verbose_name="measurement unit"
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    value = models.CharField("Value", max_length=10, unique=True)
    name = models.CharField("Visible name", max_length=25, unique=True)
    color = models.CharField("Color", max_length=10)

    def __str__(self):
        return self.name


class RecipeManager(models.Manager):
    @staticmethod
    def tag_filter(tags):
        if tags:
            return Recipe.objects.filter(tag__name__in=tags).distinct()
        else:
            return Recipe.objects.all()


class FavoriteRecipeManager(models.Manager):
    @staticmethod
    def favorite_recipe(user, tags):
        favorite = FavoriteRecipe.objects.filter(user=user).all()
        recipes_id = favorite.values_list("recipe", flat=True)
        favorite_list = (
            Recipe.objects.tag_filter(tags)
            .filter(pk__in=recipes_id)
            .order_by("-pub_date")
        )
        return favorite_list


class Recipe(models.Model):
    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"
        ordering = ["-pub_date"]

    name = models.CharField(
        max_length=200,
        verbose_name="recipe's name"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="recipes"
    )
    tag = models.ManyToManyField(
        Tag, through="RecipeTags",
        related_name="recipes"
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        through_fields=("recipe", "ingredient"),
        verbose_name="ingredients",
    )
    description = models.TextField()
    pub_date = models.DateTimeField(
        auto_now=True,
        db_index=True,
        verbose_name="publishing date"
    )
    cook_time = models.PositiveSmallIntegerField(
        verbose_name="cook time",
        null=False,
        default=10,
        help_text="Add cook time in minutes",
    )
    picture = models.ImageField(
        upload_to="recipe/",
        verbose_name="picture of the recipe"
    )
    objects = RecipeManager()

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="recipe_unique"
            )
        ]
        verbose_name = "Recipe Ingredient"
        verbose_name_plural = "Recipes Ingredients"
        ordering = ["recipe"]

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name="recipe_ingredient"
    )

    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.PROTECT,
        related_name="recipe_ingredient"
    )

    weight = models.PositiveSmallIntegerField(
        verbose_name="ingredient weight",
        null=False,
        default=10,
        help_text="Add needed weight for the recipe",
    )

    def __str__(self):
        return self.ingredient.name


class RecipeTags(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "tag"], name="recipetag_unique"
            )
        ]
        verbose_name = "Recipe tags"
        verbose_name_plural = "Recipe tags"

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Recipe title",
        related_name="recipetag",
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name="Tag name",
        related_name="recipetag",
    )


class FavoriteRecipe(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="favorite_unique"
            )
        ]
        verbose_name = "Favorite Recipe"
        verbose_name_plural = "Favorite Recipes"
        ordering = ["user"]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="favorite_by"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name="favorite"
    )
    objects = FavoriteRecipeManager()

    def __str__(self):
        return f"favorite recipe - {self.recipe.name}"


class Follow(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"],
                name="follow_unique"
            )
        ]
        ordering = [
            "-id",
        ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )


class Purchase(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="purchase_unique"
            )
        ]
        verbose_name = "Shopping List"
        verbose_name_plural = "Shopping Lists"
        ordering = ["recipe"]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="purchases"
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
