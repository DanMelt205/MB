from django import template
import decimal

register = template.Library()


@register.filter()
def subtract(value, arg):
    return value - arg


@register.filter()
def addfloats(value, arg):
    return value + arg
