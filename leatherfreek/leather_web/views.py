from django.shortcuts import render , get_object_or_404
from .models import Display_Product, Home_Product, ProductImage, Color, Catagory, Design_Catagory

# Create your views here.

def home(request):
    return render(request, 'events/index.html')

def index_trial(request):
    return render(request, 'events/index_trial.html')


def product_card(request, product_id):
    # Retrieve the product object using the product_id
    product = get_object_or_404(Display_Product, pk=product_id)
    
    # Example of passing product to the template
    context = {
        'product': product,
    }
    print(context)
    
    print(context)
    return render(request, 'events/product_card.html', context)
