from django import template

register = template.Library()


@register.filter
def index(indexable, i):
    return indexable[i]


@register.filter
def get_item(queryset):
    return queryset.total_rooms
