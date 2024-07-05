from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .models import Display_Product, shopping_cart , User_Record , Coupon , Checkout , CheckoutItem
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



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



@csrf_exempt
def apply_coupon_code_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            coupon_code = data.get('coupon_code')
            grand_total = float(data.get('grand_total'))
            print(f'Coupon code: {coupon_code}')
            print(f'Grand total: {grand_total}')

            coupon = Coupon.objects.filter(code=coupon_code).first()
            print(coupon)
            
            if coupon:
                # Apply any discount or validation logic here
                if coupon.discount_type == 'percentage':
                    discount_amount = coupon.discount_value 
                    #convert discount_amount to float
                    discount_amount = float(discount_amount)
                    grand_total -= (grand_total * discount_amount) / 100
                    grand_total -= discount_amount
                elif coupon.discount_type == 'fixed':
                    grand_total -= coupon.discount_value
                elif coupon.discount_type == 'gift':
                    # You can add the gift item to the cart here
                    pass
                else:
                    return JsonResponse({'success': False, 'error': 'Invalid coupon type'})
                
                print('Grand total after discount:', grand_total)
                
                return JsonResponse({'success': True, 'grand_total': float(grand_total)})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid coupon code'})
        except json.JSONDecodeError as e:
            print('JSON decode error:', e)
            return JsonResponse({'success': False, 'error': 'Invalid JSON'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})



def checkout_cart_ajax(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'User not authenticated'})

    cart_items = shopping_cart.objects.filter(user=request.user)
    if cart_items.count() < 1:
        return JsonResponse({'success': False, 'error': 'No items in cart'})

    try:
        data = json.loads(request.body.decode('utf-8'))
        coupon_code = data.get('coupon_code')
        coupon = Coupon.objects.filter(code=coupon_code).first()
        
        subtotal = sum(item.product.product_price * item.quantity for item in cart_items)

        subtotal = float(subtotal)

        print('Subtotal:', subtotal)
        discount_amount = 0

        if coupon:
            if coupon.discount_type == 'percentage':
                discount = coupon.discount_value 
                #convert discount_amount to float
                discount_amount = float(discount)
                discount_amount = (subtotal * discount_amount) / 100

            elif coupon.discount_type == 'fixed':
                discount_amount = coupon.discount_value
                discount_amount = float(discount_amount) 

        total_price = subtotal - discount_amount
        shipping_cost = 10  # Example shipping cost
        tax_amount = total_price * 0.1  # Example tax amount
        grand_total = total_price + shipping_cost + tax_amount


        print('Discount amount:', discount_amount)
        print('Grand total:', grand_total)
        

        checkout = Checkout.objects.create(
            user=request.user,
            total_price=subtotal,
            coupon=coupon if coupon else None,
            coupon_discount=discount_amount,
            grand_total=grand_total,
            payment_method=data.get('payment_method', 'Not specified')
        )

        for item in cart_items:
            CheckoutItem.objects.create(
                checkout=checkout,
                product=item.product,
                quantity=item.quantity,
                item_price=item.product.product_price
            )

        cart_items.delete()  # Clear the cart after checkout

        return JsonResponse({'success': True, 'checkout_id': checkout.checkout_id, 'grand_total': grand_total})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})                    









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


