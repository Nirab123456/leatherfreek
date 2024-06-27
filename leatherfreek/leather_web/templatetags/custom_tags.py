# yourapp/templatetags/home_product_tags.py
from django import template
from ..models import Home_Product , Instagram_Post

register = template.Library()

@register.simple_tag
def get_home_products():
    return Home_Product.objects.all()

@register.simple_tag
def get_home_instagram_posts():
    if Instagram_Post.objects.filter(home_page_available=True).exists():
        return Instagram_Post.objects.filter(home_page_available=True)