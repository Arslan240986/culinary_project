from culinary_project.celery import app
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import DishComment, Dish


@app.task
def comment_add(meal_id, user_id):
    """Задача отправки email-уведомлений при успешном оформлении заказа."""
    dish = Dish.objects.get(id=meal_id)
    user = User.objects.get(id=user_id)
    subject = f'Пользователь: {user} добавиль коммент'
    message = f'Пользователь: {user.profile.first_name} добавиль коммент на {dish.title} рецепт.'
    mail_sent = send_mail(subject, message, 'ushefa1ru@gmail.com.com', ['arslan092486gmail.com'])
    return mail_sent
