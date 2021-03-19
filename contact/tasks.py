from culinary_project.celery import app
from django.core.mail import send_mail
from culinary_recipe.models import Dish
from .models import UserProfile


@app.task
def send_subscribe(email):
    subject = 'dorogoy'
    message = 'Vy podpisalis na rassylku receptov na sayte Yummy'

    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          [email])
    return mail_sent


@app.task
def send_success_subscribe():
    for contact in UserProfile.objects.all():
        print(contact)
        send_mail(
            'dorogoy',
            'Dorogoy {} Vy dobavili udachno novy retcept'.format(contact.first_name),
            'admin@myshop.com',
            [contact.email],
            fail_silently=False
        )

