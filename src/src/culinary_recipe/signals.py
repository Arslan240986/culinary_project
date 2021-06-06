from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DishComment
from .tasks import comment_add


@receiver(post_save, sender=DishComment)
def post_save_create_comment(sender, instance, **kwargs):
    comment = len(DishComment.objects.all().filter(status=True))
    if comment == 10 or comment == 15 or comment==20:
        comment_add.delay(comments=comment)