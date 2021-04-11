from django import template

register = template.Library()


@register.filter
def get_by_index(indexable, i):
    try:
        result = indexable[i]
    except IndexError:
        result = ""
    return result
