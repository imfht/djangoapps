from django import template

register = template.Library()


@register.filter
def stripleadingzero(string):
    return string.lstrip('0')