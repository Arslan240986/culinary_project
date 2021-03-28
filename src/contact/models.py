from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse

from django.utils.text import slugify

from culinary_recipe.models import Dish


class UserProfileManager(models.Manager):

    def get_all_profile_to_invite(self, sender):
        profiles = UserProfile.objects.all().exclude(user=sender)
        profile = UserProfile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))

        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted' or rel.status == 'send':
                accepted.add(rel.sender)
                accepted.add(rel.receiver)

        available = [profile for profile in profiles if profile not in accepted]
        return available

    def get_all_profiles(self, me):
        profiles = UserProfile.objects.all().exclude(user=me)
        return profiles

GENDERS = [
    ('М', 'Мужчина'),
    ('Ж', 'Женщина'),
]


def get_profile_image_filepath(self, fileName):
    return f'users/{self.pk}/{"profile_image.png"}'


class UserProfile(models.Model):
    """ Персональные данные пользователя"""
    user = models.OneToOneField(User, verbose_name='Профиль пользователя', on_delete=models.CASCADE,
                                related_name='profile')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Имя для урл')
    first_name = models.CharField(verbose_name='Имя', max_length=200, blank=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=200, blank=True)
    email = models.EmailField(verbose_name='Маил', blank=True, max_length=250)
    country_of_birth = models.CharField(verbose_name='Страна проживания', blank=True, null=True, max_length=150)
    birth_date = models.DateField(auto_now=False, null=True, blank=True, verbose_name='Дата рождения')
    avatar = models.ImageField(upload_to=get_profile_image_filepath, blank=True, default='avatar_man.png', verbose_name='Аватар профиль')
    gender = models.CharField(verbose_name='Пол', max_length=1, choices=GENDERS)
    friends = models.ManyToManyField(User, verbose_name='Друзья', blank=True, related_name='friends')
    profession = models.TextField(max_length='1000', verbose_name='Профессия', help_text='Это поле необезательное', blank=True)
    interest = models.TextField(max_length='1000', verbose_name='Интересы', help_text='Это поле необезательное', blank=True)
    about = models.TextField(max_length='1000', verbose_name='О себе', help_text='Это поле необезательное', blank=True)
    dishes = models.ManyToManyField(Dish, blank=True)
    get_news_from = models.BooleanField(default=False, verbose_name="Получать уведомления", )
    get_notification_about_comments = models.BooleanField(default=False, verbose_name="Получать уведомления о комментах", )
    get_notification_friend_request = models.BooleanField(default=False, verbose_name="Получать уведомления на добавление в дружбу",)
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    objects = UserProfileManager()

    def __str__(self):
        return 'Profile for {}, {}'.format(self.user.username, self.created.strftime('%d-%m-%Y'))

    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name

    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug == '':
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name)+' '+ str(self.last_name))
                ex = UserProfile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug+" "+str(self.pk))
                    ex = UserProfile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)

    def get_privet_messages_absolute_url(self):
        return reverse('private_chat:chat_room', args=[self.slug])

    def get_friends(self):
        return self.friends.all()

    def get_friends_total_number(self):
        return self.friends.all().count()

    def get_total_friend_request(self):
        qs = self.receiver.filter(status='send')
        result = len(list(map(lambda x: x.sender, qs)))
        return result

    def get_absolute_url_for_friends(self):
        return reverse('contact:profile_detail_view', args=[self.slug])

    def get_absolute_url_for_friends_view(self):
        return reverse('contact:all_profiles_friends_view', args=[self.slug])

    def get_user_profile_detail_absolute_url(self):
        return reverse('contact:profile_detail_view', args=[self.slug])

    def get_personal_absolute_url(self):
        return reverse('contact:personal_page', args=[self.slug])

    def get_personal_draft_page_absolute_url(self):
        return reverse('contact:personal_draft_page', args=[self.slug])

    def get_dish_book_absolute_url(self):
        return reverse('contact:user_dish_book', args=[self.slug])

    def get_total_recipe_moderator_false(self):
        return Dish.objects.filter(draft=False, author=self.user, moderator=False).count()

    def get_total_draft(self):
        return Dish.objects.filter(draft=True, author=self.user).count()

    def get_total_book(self):
        return self.dishes.all().count()

    def get_total_user_recipe(self):
        return self.user.dish.filter(draft=False, author=self.user, moderator=True).count()

    def get_total_dishes(self):
        return self.user.dish.all().count()

    def get_total_number_likes_of_dishes(self):
        dishes = self.user.dish.all()
        total_likes=0
        for item in dishes:
            total_likes += item.likes.all().count()
        return total_likes

    def get_total_posts_number(self):
        return self.culinary_post.all().count()

    def get_total_posts(self):
        return self.culinary_post.all()

    def get_all_likes_given_to_posts(self):
        likes = self.postlike_set.all()
        total_likes = 0
        for item in likes:
            if item.value == 'Like':
                total_likes += 1
        return total_likes

    def get_all_likes_given_to_dishes(self):
        likes = self.dish.all()
        total_likes = 0
        for item in likes:
            if item.value == 'Like':
                total_likes += 1
        return total_likes

    def get_total_received_likes(self):
        posts = self.culinary_post.all()
        total_likes = 0
        for item in posts:
            total_likes += item.liked.all().count()
        return total_likes

USER_STATUS = [
    ('send', 'send'),
    ('accepted', 'accepted')
]


class RelationshipManager(models.Manager):

    def invitations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs


class Relationship(models.Model):
    """Отношения между пользовательями"""
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Отправитель', related_name='sender')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Получатель', related_name='receiver')
    status = models.CharField(verbose_name='Статус', max_length=9, choices=USER_STATUS)
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    objects = RelationshipManager()

    def __str__(self):
        return f'{self.sender} - {self.status} - {self.receiver}'


class ContactSubscribe(models.Model):
    """Модель подписки по email """
    email = models.EmailField(unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('home')