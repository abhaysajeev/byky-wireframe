from django import template

register = template.Library()


@register.filter(name="get")
def get(mapping, key):
    """Dict lookup by variable key, for the spec-driven grid."""
    if hasattr(mapping, "get"):
        return mapping.get(key, "")
    return getattr(mapping, key, "")
