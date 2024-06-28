# yourapp/templatetags/home_product_tags.py
from django import template
from ..models import Home_Product , Instagram_Post ,contact_us
from ..forms import ContactForm


register = template.Library()

@register.simple_tag
def get_home_products():
    return Home_Product.objects.all()

@register.simple_tag
def get_home_instagram_posts():
    if Instagram_Post.objects.filter(home_page_available=True).exists():
        return Instagram_Post.objects.filter(home_page_available=True)
    



@register.simple_tag
def handle_contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return True  # Return True to indicate successful submission
    return False  # Return False if form submission failed or if request method is not POST