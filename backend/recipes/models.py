from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    """Ингредиенты рецепта."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента')
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Tag(models.Model):
    """Теги рецепта."""
    name = models.CharField(
        unique=True,
        max_length=200,
        verbose_name='Название тега')
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет тега в HEX формате',
        unique=True,
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Формат цвета не соответствует HEX')]
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Рецепт."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор')
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта')
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение')
    text = models.TextField(
        verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name='Ингредиенты')
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=(
            MinValueValidator(
                1,
                message='Время приготовления должно быть больше 0'),)
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания')
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Ингредиенты рецепта."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients')
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients')
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиента',
        default=1,
        validators=(
            MinValueValidator(
                1,
                message='Количество ингредиента должно быть больше 0'),))

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient')]

    def __str__(self):
        return f'{self.ingredient.name} {self.amount}'


class FavouriteRecipe(models.Model):
    """Любимые рецепты."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Любимый рецепт')

    class Meta:
        verbose_name = 'Любимый рецепт'
        verbose_name_plural = 'Любимые рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favourite_recipe')]

    def __str__(self):
        return (f'Пользователь {self.user} добавил '
                f'рецепт {self.recipe} в избранное')


class ShoppingCart(models.Model):
    """Корзина."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт в корзине')

    class Meta:
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_shopping_cart')
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Корзину покупок'
