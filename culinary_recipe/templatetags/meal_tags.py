from django import template
from ..models import Category, Dish


register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('culinary_recipe/tags/last_dishes.html')
def get_last_dishes():
    dishes = Dish.objects.order_by('-id').filter(draft=False, moderator=True)[:5]
    return {'last_dishes': dishes}
