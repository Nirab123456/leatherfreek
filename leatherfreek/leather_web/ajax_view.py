from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .models import Display_Product, shopping_cart

@require_POST
def add_to_cart_ajax(request, product_id):
    product = get_object_or_404(Display_Product, product_id=product_id)
    
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # User is logged in, associate cart with user
        cart_item, created = shopping_cart.objects.get_or_create(user=request.user, product=product)

        if not created:
            # If the item already exists in the cart, increment quantity
            cart_item.quantity += 1
            cart_item.save()
    else:
        # User is not authenticated, use session-based cart
        if 'cart' not in request.session:
            request.session['cart'] = {}

        cart = request.session['cart']

        # Check if the product already exists in the session cart
        if product_id in cart:
            cart[product_id]['quantity'] += 1
        else:
            cart[product_id] = {
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



