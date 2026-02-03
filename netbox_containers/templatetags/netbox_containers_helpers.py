from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter(name="render_boolean")
def render_boolean(value):
    if value:
        return mark_safe('<span class="text-success"><i class="mdi mdi-check-bold"></i></span>')
    return mark_safe('<span class="text-danger"><i class="mdi mdi-close-thick"></i></span>')
