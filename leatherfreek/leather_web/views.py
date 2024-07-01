from django.shortcuts import render , get_object_or_404 ,redirect
from .models import Display_Product, Home_Product, Color, Catagory, Design_Catagory , shopping_cart , User_Record
from django.contrib.auth.models import User

# Create your views here.

def user_profile(request):
    if request.user.is_authenticated:
        user = request.user
        user_record, created = User_Record.objects.get_or_create(user=user)
        print('user rewcord',user_record)
        if user_record:
            return render(request, 'events/user_profile.html', {'user': user_record})
        else:        
            user_record = User.objects.filter(username=user.username).first()
            return render(request, 'events/user_profile.html', {'user': user_record})

    else:
        return redirect('user_login')
    



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


def update_profile(request):
    if request.method == 'GET':
        user = request.user
        user_record, created = User_Record.objects.get_or_create(user=user)
        print('request', request)
        
        # Update user record with data from GET parameters
        user_record.user_name = request.GET.get('user_name', user_record.user_name)
        user_record.first_name = request.GET.get('first_name', user_record.first_name)
        user_record.last_name = request.GET.get('last_name', user_record.last_name)
        user_record.user_email = request.GET.get('user_email', user_record.user_email)
        user_record.user_phone = request.GET.get('user_phone', user_record.user_phone)
        user_record.country = request.GET.get('country', user_record.country)
        user_record.city = request.GET.get('city', user_record.city)
        user_record.zip_code = request.GET.get('zip', user_record.zip_code)
        user_record.address = request.GET.get('address', user_record.address)
        
        user_record.save()
        context = {
            'user': user_record,
        } 
        return render(request, 'events/user_profile.html', context)

    else:
        user = request.user
        user_record = User_Record.objects.filter(user=user).first()
        return render(request, 'events/user_profile.html', {'user': user_record})










def about_contact(request):
    return render(request, 'events/about_contact.html')