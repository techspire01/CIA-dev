from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get a value from a dictionary using a variable key"""
    return dictionary.get(key, 0)

@register.filter
def get_subcategories(dictionary, key):
    """Get subcategories from a dictionary, return empty list if key not found"""
    return dictionary.get(key, [])

