from ckeditor.fields import RichTextField
from django.db import models
from django.core.validators import FileExtensionValidator
from contact.models import UserProfile
from django.core.exceptions import ValidationError
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from culinary_recipe.utils import watermark_photo

def validate_max_len(val):
    if len(val) < 10:
        raise ValidationError('Длина названия поста должен привышать 10 символов', code='odd', params={'value': val})


class CulinaryPost(models.Model):
    title = models.CharField(max_length=1000, verbose_name="Загаловок", blank=True,
                             validators=[validate_max_len], help_text='Заголовок должен быть минимуи 10 символов')
    content = RichTextField(verbose_name='Описания')
    image = models.ImageField(verbose_name='Фотография', upload_to='posts', blank=True, null=True)
    liked = models.ManyToManyField(UserProfile, blank=True, related_name='post_likes')
    moderator = models.BooleanField(verbose_name='Модератор', default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='culinary_post')

    def __str__(self):
        return str(self.title)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__image = self.image

    def save(self, *args, **kwargs):
        if self.image != self.__image or self.image == '':
            print('after', self.__image)
            new_name = watermark_photo(self.image, str(self.image),
                                       'static/image/logo_header.png', 'culinary_post_image', position=(10, 10))
            self.image = new_name
        super().save(*args, **kwargs)

    #  watermark_photo(instance.image, str(instance.image), 'static/image/logo_header.png', 'posts', position=(10, 10))

    def get_absolute_url(self):
        return reverse('culinary_post:culinary_post_detail_view', args=[self.pk])

    def get_update_absolute_url(self):
        return reverse('culinary_post:post_update', args=[self.pk])

    def get_delete_absolute_url(self):
        return reverse('culinary_post:post_delete', args=[self.pk])

    def get_total_likes(self):
        return self.liked.all().count()

    def get_total_comments(self):
        return self.post_comments.all().count()

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Кулинарный пост'
        verbose_name_plural = 'Кулинарные посты'


class CulinaryPostComment(MPTTModel):
    """Комментарии к постам"""
    text = models.TextField('Написать комментарии', max_length=5000)
    parent = TreeForeignKey('self', verbose_name='Родитель',
                               on_delete=models.CASCADE, related_name='children',
                               null=True, blank=True)
    post = models.ForeignKey(CulinaryPost, verbose_name='Пост', on_delete=models.CASCADE, related_name='post_comments')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Автор')
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author} -to- {self.text}'

    class MPTTMeta:
        verbose_name = 'Коментария'
        verbose_name_plural = 'Коментарии'
        ordering = ['update']
        order_insertion_by = ['update']


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class PostLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,)
    post = models.ForeignKey(CulinaryPost, on_delete=models.CASCADE,)
    value = models.CharField(max_length=12, choices=LIKE_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}-{self.post}-{self.value}'

    class Meta:
        verbose_name = ' Лайки к посте'
        verbose_name_plural = 'Лайки к постам'
