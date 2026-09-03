from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

_STATUS_BADGE_CLASSES = {
    "active": "success",
    "running": "success",
    "offline": "secondary",
    "planned": "info",
    "staged": "info",
    "failed": "danger",
}


@register.filter(name="render_boolean")
def render_boolean(value):
    if value:
        return mark_safe(
            '<span class="text-success"><i class="mdi mdi-check-bold"></i></span>'
        )
    return mark_safe(
        '<span class="text-danger"><i class="mdi mdi-close-thick"></i></span>'
    )


@register.simple_tag(name="status_badge")
def status_badge(status, display):
    """Shared Device/VM status badge for the Container/Pod/Network detail pages."""
    css_class = _STATUS_BADGE_CLASSES.get(status, "light")
    text_class = " text-body" if css_class == "light" else ""
    return mark_safe(
        f'<span class="badge text-bg-{css_class} rounded-pill{text_class}">'
        f"{escape(display)}</span>"
    )
