from django.db import models
from django.core.validators import FileExtensionValidator
from contact.models import UserProfile
from django.core.exceptions import ValidationError


def validate_max_len(val):
    if len(val) < 5:
        raise ValidationError('Число %(value)s нечетное', code='odd', params={'value': val})


class CulinaryPost(models.Model):
    title = models.CharField(max_length=1000, verbose_name="Загаловок", blank=True,
                             validators=[validate_max_len], help_text='Заголовок должен быть минимуи 10 символов')
    content = models.TextField(verbose_name='Описания')
    image = models.ImageField(verbose_name='Фотография', upload_to='posts', blank=True)
    liked = models.ManyToManyField(UserProfile, blank=True, related_name='post_likes')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='culinary_post')

    def __str__(self):
        return str(self.content[:20])

    def get_total_likes(self):
        return self.liked.all().count()

    def get_total_comments(self):
        return self.postcomment_set.all().count()

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Кулинарный пост'
        verbose_name_plural = 'Кулинарные посты'


class PostComment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='culinary_comment')
    post = models.ForeignKey(CulinaryPost, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Коментария к посту'
        verbose_name_plural = 'Коментарии к постам'


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
