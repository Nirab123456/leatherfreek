# yourapp/templatetags/home_product_tags.py
from django import template
from ..models import Home_Product , Instagram_Post ,contact_us
from ..forms import ContactForm
from ..auto_emails import contact_form_recived_mail
from django.contrib.auth.models import User

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
            #if email is available in the form
            if 'contact_email' in form.cleaned_data:
                email = form.cleaned_data['contact_email']
                name  = form.cleaned_data['contact_name']
                message = form.cleaned_data['contact_message']
                print(email)
                contact_form_recived_mail(email,name,message)



                form.save()  # Save the form data to the database
                return 'Your massage has been send. Thank you'
        
    return  'Send a Text to us'



@register.filter
def multiply(value, arg):
    return value * arg


            