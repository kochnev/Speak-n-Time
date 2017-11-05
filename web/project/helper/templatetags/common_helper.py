from django import template
from main.models import Language
register = template.Library()

@register.filter('get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter('language_display')
def language_display(id):
    return Language.objects.get(id=id).name