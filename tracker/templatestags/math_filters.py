# tracker/templatetags/math_filters.py
from django import template

# Register the template library
register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplies the value by the argument."""
    try:
        # Convert both to float for accurate multiplication
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def div(value, arg):
    """Divides the value by the argument. Returns 0 on division by zero."""
    try:
        # Check for division by zero
        if float(arg) == 0:
            return 0
        return float(value) / float(arg)
    except (ValueError, TypeError):
        return 0