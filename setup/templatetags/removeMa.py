from django import template

register = template.Library()

def removeMa(value):
    return value[:-2]