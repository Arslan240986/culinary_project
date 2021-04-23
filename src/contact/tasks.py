from culinary_project.celery import app
from django.contrib.auth.models import User
from django.core.mail import send_mail

from culinary_project import settings


@app.task
def send_subscribe(email):
    subject = 'Подписка на рассылку'
    message = 'Вы успешно подписались на рассылку на сайте У-шефа'

    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          [email])
    return mail_sent


@app.task
def send_success_subscribe(**kwargs):
    author = User.objects.get(id=kwargs['author'])
    send_mail(
        'Успешно пройдена проверка',
        f'Дорогой {author.profile.first_name} Ваш рецепт {kwargs["title"]} упешно прошла проверку и добавлен на сайт',
        settings.EMAIL_HOST_USER,
        [author.profile.email],
        fail_silently=False
    )

