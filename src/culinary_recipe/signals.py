from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DishComment
from .tasks import comment_add


@receiver(post_save, sender=DishComment)
def post_save_create_comment(sender, instance, **kwargs):
    user_id = instance.author.id
    meal = instance.meal
    comment_add.delay(meal.id, user_id)