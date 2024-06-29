from django.shortcuts import render , get_object_or_404
from .models import Display_Product, Home_Product, Color, Catagory, Design_Catagory , shopping_cart

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
        'volume_description' : product.volume_description,
    }
    print(context)
    
    print(context)
    return render(request, 'events/product_card.html', context)

def view_products(request, catagory_id):
    # Retrieve the catagory object using the catagory_id
    catagory = get_object_or_404(Catagory, pk=catagory_id)
    
    # Retrieve all products in the catagory
    products = Display_Product.objects.filter(product_catagory=catagory)
    
    # Example of passing products to the template
    context = {
        'catagory': catagory,
        'products': products,
    }
    
    return render(request, 'events/view_products.html', context)


def user_profile(request):
    return render(request, 'events/user_profile.html')

def user_signup(request):
    return render(request, 'accounts/signup.html')

def user_logout(request):
    return render(request, 'accounts/logout.html')

def user_login(request):
    return render(request, 'accounts/login.html')

def shopping_cart_view(request):
    if request.user.is_authenticated:
        user = request.user
        cart_items = shopping_cart.objects.filter(user=user)
        context = {
            'cart_items': cart_items,
        }

    elif 'cart' in request.session:
        cart = request.session['cart']
        cart_items = []
        for product_id in cart:
            product = get_object_or_404(Display_Product, pk=product_id)
            cart_items.append({
                'product': product,
                'quantity': cart[product_id]['quantity'],
            })

        context = {
            'cart_items': cart_items,
        }
    else:
        context = {}

    return render(request, 'events/shopping_cart.html', context)

















def about_contact(request):
    return render(request, 'events/about_contact.html')