from django import template
from django.conf import settings

register = template.Library()


@register.filter
def normalize_table_number(value, arg):
    return value + settings.PAGE_SIZE * (arg - 1)
