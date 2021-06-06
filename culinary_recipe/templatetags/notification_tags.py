from django import template

register = template.Library()


@register.simple_tag()
def new_messages_not(*args):
    pass