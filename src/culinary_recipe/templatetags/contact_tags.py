from django import template

register = template.Library()


@register.inclusion_tag('contact/tags/form.html')
def contact_form():
    pass