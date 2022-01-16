from culinary_project.celery import app
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import DishComment, Dish
from culinary_project import settings


@app.task
def comment_add(**kwargs):
    """Задача отправки email-уведомлений при успешном оформлении заказа."""
    comments = DishComment.objects.all().filter(status=True)
    subject = f'Дорогой модератор у вас {kwargs["comments"]} не проверенных комментариев пожалуйста проверте их в скором времени'
    message = ''
    for comment in comments:
        message += f'(Пользователь: {comment.author.profile.first_name} добавиль коммент на {comment.meal.title} рецепт. коммент {comment.text}) ,'
    mail_sent = send_mail(subject, message, settings.SERVER_EMAIL, ['arslan092486gmail.com'])
    return mail_sent