from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from .utils import make_slug, watermark_photo
# from contact.tasks import send_success_subscribe
import uuid


def get_random_code():
    code = str(uuid.uuid4())[:8].replace('-', '').lower()
    return code


class Country(models.Model):
    """Страны"""
    name = models.CharField('Страна', max_length=250)
    slug = models.SlugField(max_length=250, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('culinary_recipe:by_country', args=[self.slug, self.pk])

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ('name',)


class Category(models.Model):
    """Категории"""
    name = models.CharField('Категория', max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    poster = models.ImageField(verbose_name='Постер для категории', upload_to='category/')

    def get_absolute_url(self):
        return reverse('culinary_recipe:cats_list', args=[self.slug])

    def __str__(self):
        return self.name

    def get_meals(self):
        return self.dish_set.all()[:3]

    def save(self, *args, **kwargs):
        if self.poster:
            new_steps_name = watermark_photo(self.poster, str(self.poster),
                            'static/image/logo_header.png', 'category', position=(10, 10))
            self.poster = new_steps_name
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class SubCategory(models.Model):
    """Категории"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_category',
                                 verbose_name='Подкатегория')
    name = models.CharField('Категория', max_length=250)
    slug = models.SlugField(max_length=250, unique=True, verbose_name='Поле для урл')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('culinary_recipe:last_list', args=[self.slug])

    def get_last_three_dishes(self):
        return self.dish_set.all().filter(moderator=True, draft=False)[:3]

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ('name',)


class Technology(models.Model):
    """Технология"""
    name = models.CharField(max_length=150, verbose_name='Названия технологии')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Поле для урл')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Технология'
        verbose_name_plural = 'Технологии'
        ordering = ('name',)


class Occasion(models.Model):
    """Повод"""
    name = models.CharField(max_length=150, verbose_name='Повод')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Поле для урл')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Повод'
        verbose_name_plural = 'Поводы'
        ordering = ('name',)


class Device(models.Model):
    """Устройтсво"""
    name = models.CharField(max_length=150, verbose_name='Названия устройтсва')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Поле для урл')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройства'
        ordering = ('name',)


class Complexity(models.Model):
    """Повод"""
    name = models.CharField(max_length=150, verbose_name='Сложность приготовления')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Поле для урл')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сложность приготовления'
        verbose_name_plural = 'Сложность приготовления'
        ordering = ('name',)


class Vegeterian(models.Model):
    """Повод"""
    name = models.CharField(max_length=150, verbose_name='Вегетарианство')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Поле для урл')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вегетарианство'
        verbose_name_plural = 'Вегетарианство'


def get_poster_image_filepath(self, fileName):
    return f'meal/{self.slug[0:30]}/poster/{fileName}'


def get_steps_image_filepath(self, fileName):
    return f'meal/{self.meal.pk}/steps/{fileName}'

from django.dispatch import Signal


class Dish(models.Model, HitCountMixin):
    """Блюдо"""
    title = models.CharField(verbose_name='Название', max_length=700)
    slug = models.SlugField(max_length=300, unique=True, verbose_name='Поле для урл')
    description = RichTextField(verbose_name='Описание')
    poster = models.ImageField('Постер', upload_to=get_poster_image_filepath)
    category = models.ForeignKey(Category, verbose_name='Категория',
                                 on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True,
                                     verbose_name='Подкатегория')
    country = models.ForeignKey(Country, verbose_name='Страна', on_delete=models.SET_NULL,
                                null=True, help_text='(необязательное поле)')
    preparation_time_hour = models.PositiveSmallIntegerField(verbose_name='Время подготовки', blank=True, null=True)
    preparation_time_minute = models.PositiveSmallIntegerField(blank=True, null=True)
    cooking_time_hour = models.PositiveSmallIntegerField(verbose_name='Время готовки', blank=True, null=True)
    cooking_time_minute = models.PositiveSmallIntegerField(blank=True, null=True)
    servings = models.CharField(verbose_name='Количество порций', max_length=100, blank=True, null=True)
    complexity = models.ForeignKey(Complexity, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Сложность приготовления')
    vegetarian = models.ForeignKey(Vegeterian, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Вегетарианство')
    technology = models.ManyToManyField(Technology, blank=True, verbose_name='Технология')
    occasion = models.ManyToManyField(Occasion, blank=True, verbose_name='Повод')
    device = models.ManyToManyField(Device, blank=True, verbose_name='Устройтво')
    calorie = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Калория')
    protein = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Протеин')
    fat = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Жиры')
    carbohydrate = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Углеводы')
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.SET_NULL,
                               related_name='dish', null=True)
    draft = models.BooleanField(verbose_name='Черновик', default=False)
    moderator = models.BooleanField(verbose_name='Модератор', default=False)
    advice = RichTextField(verbose_name="Полезные советы", blank=True,)
    likes = models.ManyToManyField(User, verbose_name='Лайк', related_name='meal_likes')
    is_liked = models.BooleanField(default=False)
    dish_added = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')

    def __str__(self):
        return self.title

    def current_hit_count(self):
        return self.hit_count.hits

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__title = self.title
        self.__poster = self.poster

    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if self.title != self.__title or self.slug == '':
            if self.title:
                to_slug = make_slug(str(self.title))+"-"+get_random_code()
                ex = Dish.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = make_slug(to_slug)+"-"+get_random_code()
                    ex = Dish.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        if self.poster != self.__poster or self.poster == '':
            new_name = watermark_photo(self.poster, str(self.poster),
                                       'static/image/logo_header.png', f'meal/{self.slug[0:30]}/poster', position=(10, 10))
            self.poster = new_name
        super().save(*args, **kwargs)

    def get_total_likes(self):
        return self.dish_like.filter(value="Like").count()

    def get_absolute_url(self):
        return reverse('culinary_recipe:detail_view', args=[self.slug, self.pk])

    def get_update_absolute_url(self):
        return reverse('culinary_recipe:update_meal', args=[self.slug])

    def get_delete_absolute_url(self):
        return reverse('culinary_recipe:delete_meal', args=[self.pk])

    def get_comments(self):
        return self.comments.all()

    def get_total_comments(self):
        return self.comments.filter(status=False).count()

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class DishLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='dish_like')
    value = models.CharField(max_length=12, choices=LIKE_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}-{self.dish}-{self.value}'

    class Meta:
        verbose_name = 'Лайки к рецепту'
        verbose_name_plural = 'Лайки к рецептам'


class Measure(models.Model):
    """Мера веса/объема"""
    name = models.CharField(verbose_name='Мера веса/объема', max_length=15)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Мера веса/объема'


class IngredientTitle(models.Model):
    name = models.CharField(max_length=250, verbose_name='Заголовок ингредиента')
    meal = models.ForeignKey(Dish, verbose_name='Блюдо', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Заголовок ингредиента'
        verbose_name_plural = 'Заголовок ингредиентов'


class IngredientList(models.Model):
    """Ингредиент"""
    title = models.ForeignKey(IngredientTitle, verbose_name='Заголовок ингредиента', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField( verbose_name='Название', max_length=25)
    quantity = models.CharField(max_length=150, verbose_name='Количество', blank=True)
    measure = models.ForeignKey(Measure, verbose_name='Мера веса/объема', on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(verbose_name='Примечание', null=True, blank=True)

    def __str__(self):
        return f'{self.name}-{self.title}'

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Step(models.Model):
    """Пошаговый рецепт"""
    description = models.TextField(verbose_name='Описание', null=True )
    meal = models.ForeignKey(Dish, verbose_name='Блюдо', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(verbose_name='Фото', upload_to=get_steps_image_filepath, null=True, blank=True)

    def __str__(self):
        return f'{self.pk} - {self.meal.title}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__image = self.image

    def save(self, *args, **kwargs):
        if self.__image != self.image or self.image == '':
            new_steps_name = watermark_photo(self.image, str(self.image),
                            'static/image/logo_header.png',f'meal/{self.meal.pk}/steps', position=(10, 10))
            self.image = new_steps_name
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['id']
        verbose_name = 'Пошаговый рецепт'
        verbose_name_plural = 'Пошаговые рецепты'


class DishComment(MPTTModel):
    """Отзывы"""
    text = models.TextField('Написать комментарии', max_length=5000)
    parent = TreeForeignKey('self', verbose_name='Родитель',
                               on_delete=models.CASCADE, related_name='children',
                               null=True, blank=True)
    meal = models.ForeignKey(Dish, verbose_name='Блюдо', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Автор')
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.author} -to- {self.text}'

    class MPTTMeta:
        ordering = ['created']
        order_insertion_by = ['created']
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментария'
