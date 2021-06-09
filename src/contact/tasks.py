from culinary_project.celery import app
from django.contrib.auth.models import User
from django.core.mail import send_mail

from culinary_project import settings

from contact.models import UserProfile


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
        settings.SERVER_EMAIL,
        [author.profile.email],
        fail_silently=False
    )


@app.task
def notice_about_new_messages(**kwargs):
    sender = UserProfile.objects.get(id=kwargs['sender'])
    receiver = UserProfile.objects.get(id=kwargs['receiver'])
    mail_sent = send_mail(
        'Успешно пройдена проверка',
        f'Дорогой {receiver.first_name} Вам  {sender.first_name} на сайте У-шефа отправил сообшения для прочтения пройдите пожалуйста по ссылке\n https://ushefa.ru{receiver.get_absolute_url_for_friends_view()}',
        settings.EMAIL_HOST_USER,
        [receiver.email],
        fail_silently=False
    )
    return mail_sent

