from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название ингредиента')
    measurement_unit = models.CharField(max_length=200, verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Tag(models.Model):
    name = models.CharField(
        unique=True,
        max_length=200, 
        verbose_name='Название тега')
    color = models.CharField(
        max_length=7, 
        verbose_name='Цвет тега')
    slug = models.SlugField(
        unique=True, 
        verbose_name='Слаг')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('-id',)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, 
        related_name='recipes', 
        verbose_name='Автор')
    name = models.CharField(
        max_length=200, 
        verbose_name='Название рецепта')
    image = models.ImageField(
        upload_to='static/recipes/', 
        verbose_name='Изображение')
    text = models.TextField(
        verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient, 
        through='RecipeIngredient', 
        verbose_name='Ингредиенты')
    tags = models.ManyToManyField(
        Tag, 
        related_name='recipes', 
        verbose_name='Теги')
    cooking_time = models.PositiveSmallIntegerField(verbose_name='Время приготовления')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('id',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
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
            validators.MinValueValidator(
                1,
                message='Количество ингредиента должно быть больше 0')),
                verbose_name='Количество ингредиента')


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

class Subscription(models.Model):
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='following', 
        verbose_name='Автор')
    subscriber = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='follower', 
        verbose_name='Подписчик')
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата подписки')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'subscriber'],
                name='unique_subscription')]

    def __str__(self):
        return f'Пользователь {self.subscriber} подписан на {self.author}'


class FavoriteRecipe(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='favorite_recipes', 
        verbose_name='Пользователь')
    recipe = models.ManyToManyField(
        Recipe, 
        on_delete=models.CASCADE, 
        related_name='favorite_recipes', 
        verbose_name='Любимый рецепт')

    class Meta:
        verbose_name = 'Любимый рецепт'
        verbose_name_plural = 'Любимые рецепты'


    def __str__(self):
        return f'Пользователь {self.user} добавил рецепт {self.recipe} в избранное'

    @receiver(post_save, sender=User)
    def create_favorite_recipe(sender, instance, created, **kwargs):
        if created:
            return FavoriteRecipe.objects.create(user=instance)


class ShoppingCart(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='shopping_cart', 
        null=True,
        verbose_name='Пользователь')
    recipe = models.ManyToManyField(
        Recipe,
        related_name='shopping_cart', 
        verbose_name='Рецепт в корзине')

    class Meta:
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'
        ordering = ('-id',)

    def __str__(self):
        list_ = [item['name'] for item in self.recipe.values('name')]
        return f'Пользователь {self.user} добавил {list_} в корзину'

    @receiver(post_save, sender=User)
    def create_shopping_cart(sender, instance, created, **kwargs):
        if created:
            return ShoppingCart.objects.create(user=instance)