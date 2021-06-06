from django import template
from contact.forms import ContactSubscribeForm

register = template.Library()


@register.inclusion_tag('contact/tags/form.html')
def contact_form():
    return {'contact_form': ContactSubscribeForm()}