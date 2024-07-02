from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .models import Display_Product, shopping_cart , User_Record

def add_to_cart_ajax(request, product_id):
    product = get_object_or_404(Display_Product, product_id=product_id)
    
    if request.user.is_authenticated:
        # User is logged in
        try:
            # Try to get the existing cart item
            cart_item = shopping_cart.objects.get(user=request.user, product=product)
            # If it exists, increase the quantity by 1
            cart_item.quantity += 1
        except shopping_cart.DoesNotExist:
            # If it doesn't exist, create a new cart item with quantity 1
            cart_item = shopping_cart(user=request.user, product=product, quantity=1)
        
        # Save the cart item
        cart_item.save()
    else:
        # User is not authenticated, use session-based cart
        if 'cart' not in request.session:
            request.session['cart'] = {}

        cart = request.session['cart']

        # Check if the product already exists in the session cart
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1
        else:
            cart[str(product_id)] = {
                'product_id': product_id,
                'quantity': 1,
                # You can also store other product details in the session if needed
            }

        # Save the updated session cart
        request.session.modified = True
        print(request.session['cart'])

    return JsonResponse({'success': True, 'product': product.product_name})

def increase_quantity_ajax(request, product_id):
    product = get_object_or_404(Display_Product, product_id=product_id)
    
    if request.user.is_authenticated:        
        cart_item = shopping_cart.objects.filter(user=request.user, product=product).first()
        if cart_item:
            cart_item.quantity += 1
            cart_item.save()
        else:
            return JsonResponse({'success': False, 'message': 'Cart item not found'}, status=404)
    else:
        cart = request.session.get('cart', {})
        
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1
        else:
            cart[str(product_id)] = {'quantity': 1, 'product_name': product.product_name}
        
        request.session['cart'] = cart
        request.session.modified = True

    return JsonResponse({'success': True, 'product': product.product_name})


def decrease_quantity_ajax(request, product_id):
    product = get_object_or_404(Display_Product, product_id=product_id)
    
    if request.user.is_authenticated:
        cart_item = shopping_cart.objects.filter(user=request.user, product=product).first()
        if cart_item:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            return JsonResponse({'success': False, 'message': 'Cart item not found'}, status=404)
    else:
        cart = request.session.get('cart', {})
        
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] -= 1
            if cart[str(product_id)]['quantity'] == 0:
                del cart[str(product_id)]
        else:
            return JsonResponse({'success': False, 'message': 'Cart item not found'}, status=404)
        
        request.session['cart'] = cart
        request.session.modified = True

    return JsonResponse({'success': True, 'product': product.product_name})


def remove_from_cart_ajax(request, product_id):
    product = get_object_or_404(Display_Product, product_id=product_id)
    
    if request.user.is_authenticated:
        cart_item = shopping_cart.objects.filter(user=request.user, product=product).first()
        cart_item.delete()
    else:
        cart = request.session.get('cart', {})
        
        if str(product_id) in cart:
            del cart[str(product_id)]
        else:
            return JsonResponse({'success': False, 'message': 'Cart item not found'}, status=404)
        
        request.session['cart'] = cart
        request.session.modified = True

    return JsonResponse({'success': True, 'product': product.product_name})

def update_profile_ajax(request):
    if request.method == 'GET':
        user = request.user
        user_record = get_object_or_404(User_Record, user=user)

        # Extract data from the POST request
        first_name = request.GET.get('first_name')
        last_name = request.GET.get('last_name')
        user_email = request.GET.get('user_email')
        user_phone = request.GET.get('user_phone')
        country = request.GET.get('country')
        city = request.GET.get('city')
        zip_code = request.GET.get('zip')
        address = request.GET.get('address')
        print(first_name)


        # Update the user record
        user_record.first_name = first_name
        user_record.last_name = last_name
        user_record.user_email = user_email
        user_record.user_phone = user_phone
        user_record.country = country
        user_record.city = city
        user_record.zip_code = zip_code
        user_record.address = address
        user_record.save()

        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid request method.'}, status=400)


