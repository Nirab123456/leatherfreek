# yourapp/templatetags/home_product_tags.py
from django import template
from ..models import Home_Product

register = template.Library()

@register.simple_tag
def get_home_products():
    return Home_Product.objects.all()
