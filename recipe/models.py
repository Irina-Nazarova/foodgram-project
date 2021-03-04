from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    # название ингридиента
    name = models.CharField(max_length=5000,
                            verbose_name='ingredient\'s name',
                            unique=True)
    # единица измерения
    measure = models.CharField(max_length=100,
                               verbose_name='measurement unit')

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.measure})'


class RecipeType(models.Model):
    TYPE_CHOICES = (
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    )
    type_name = models.CharField(max_length=25,
                                 choices=TYPE_CHOICES,
                                 unique=True)
    color = models.CharField(max_length=10,
                             default='',
                             editable=False)

    class Meta:
        verbose_name = 'Recipe type'
        verbose_name_plural = 'Recipe types'
        ordering = ['type_name']

    def save(self, *args, **kwargs):
        if self.type_name == 'dinner':
            self.color = 'purple'
        elif self.type_name == 'lunch':
            self.color = 'green'
        else:
            self.color = 'orange'

        super(RecipeType, self).save(*args, **kwargs)

    def __str__(self):
        return self.type_name


class Recipe(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='recipe\'s name')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes')
    type = models.ManyToManyField(RecipeType, related_name='tag')
    ingredients = models.ManyToManyField(Ingredient, related_name='ingredients',)
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now=True,
                                    db_index=True,
                                    verbose_name='publishing date')
    cook_time = models.PositiveSmallIntegerField(
        verbose_name='cook time',
        null=False,
        default=10,
        help_text='Add cook time in minutes'
    )
    picture = models.ImageField(upload_to='recipe/',
                                verbose_name='picture of the recipe')

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ['-pub_date']


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='recipe_ingredient')
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.PROTECT,
                                   related_name='recipe_ingredient')
    weight = models.PositiveSmallIntegerField(
        verbose_name='ingredient weight',
        null=False,
        default=10,
        help_text='Add needed weight for the recipe'
    )

    class Meta:
        unique_together = ('recipe', 'ingredient')
        verbose_name = 'Recipe Ingredient'
        verbose_name_plural = 'Recipes Ingredients'
        ordering = ['recipe']

    def __str__(self):
        return f'{self.ingredient.name} {self.weight} for {self.recipe.name}'


class FavoriteRecipe(models.Model):
    # Работа со списком избранного доступна только авторизованному пользователю
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite_by')

    # рецепты избранного может просматривать только его владелец
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite')

    class Meta:
        unique_together = ('recipe', 'user')
        verbose_name = 'Favorite Recipe'
        verbose_name_plural = 'Favorite Recipes'
        ordering = ['user']

    def __str__(self):
        return f'favorite recipe - {self.recipe.name}'


class Follow(models.Model):
    #  пользователь, который подписывается
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower")

    #  пользователь, на которого подписываются
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following")

    class Meta:
        ordering = ['-id', ]
        unique_together = ['user', 'author']


class Purchase(models.Model):
    # список покупок пользователя
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='purchases')

    # рецепт добавленый в список покупок
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)








