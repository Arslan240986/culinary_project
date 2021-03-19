from django import template

from contact.models import UserProfile
from private_chat.models import Thread, ChatMessage

register = template.Library()


@register.simple_tag()
def new_messages_not(*args):
    profile = UserProfile.objects.get(id=args[0])
    threads = Thread.objects.by_user(profile)
    total_msg = 0
    for thread in threads:
        msg = ChatMessage.objects.filter(thread=thread, is_readed=False).exclude(user=profile).count()
        total_msg += msg
    return total_msg