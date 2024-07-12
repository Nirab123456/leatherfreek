import os
from django.http import JsonResponse ,HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404 , render , redirect
from .models import Display_Product, shopping_cart , User_Record , Coupon , Checkout , CheckoutItem
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
import io
from django.core.mail import send_mail , get_connection , EmailMessage
from django.conf import settings
from django.core.exceptions import ValidationError
from decouple import config
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


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
        # Send the invoice email
        send_invoice_mail(request, checkout, subtotal, discount_amount, shipping_cost, tax_amount, grand_total)
        print('cart sent')

        return JsonResponse({'success': True, 'checkout_id': checkout.checkout_id, 'grand_total': grand_total})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
    
def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        result = finders.find(uri)
        if result:
                if not isinstance(result, (list, tuple)):
                        result = [result]
                result = list(os.path.realpath(path) for path in result)
                path=result[0]
        else:
                sUrl = settings.STATIC_URL        # Typically /static/
                sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                mUrl = settings.MEDIA_URL         # Typically /media/
                mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                if uri.startswith(mUrl):
                        path = os.path.join(mRoot, uri.replace(mUrl, ""))
                elif uri.startswith(sUrl):
                        path = os.path.join(sRoot, uri.replace(sUrl, ""))
                else:
                        return uri

        # make sure that file exists
        if not os.path.isfile(path):
                raise RuntimeError(
                        'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path



def convert_html_to_pdf(source_html):
    """
    Convert HTML to PDF using xhtml2pdf
    """
    buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(
        source_html, dest=buffer, link_callback=link_callback)

    if pisa_status.err:
        return None
    buffer.seek(0)
    return buffer


def send_invoice_mail(request, checkout, subtotal, discount_amount, shipping_cost, tax_amount, grand_total):
    try:
        # Render HTML template to string
        cart_items = CheckoutItem.objects.filter(checkout=checkout)
        html_content = render_to_string('account/email/invoice.html', {
            'user': request.user,
            'checkout': checkout,
            'cart_items': cart_items,
            'subtotal': subtotal,
            'discount_amount': discount_amount,
            'shipping_cost': shipping_cost,
            'tax_amount': tax_amount,
            'grand_total': grand_total
        })


        # Convert HTML to PDF using xhtml2pdf
        pdf_buffer = convert_html_to_pdf(html_content)
        print('pdf_buffer:', pdf_buffer)

        if pdf_buffer is None:
            return HttpResponse('Error generating PDF', status=500)

        # Email configuration
        my_host = config('EMAIL_HOST')
        my_port = config('EMAIL_PORT', cast=int)
        my_username = config('SUPPORT_EMAIL')
        my_password = config('EMAIL_HOST_PASSWORD')
        my_use_tls = True
        my_use_ssl = False
        my_from_email = config('SUPPORT_EMAIL')
        my_recipient_list = [request.user.email]
        my_subject = 'Your Purchase Receipt'
        my_message = 'Thank you for your purchase. Please find the attached receipt.'
        my_html_message = render_to_string('auto_emails/about_contact_auto_email.html')
        my_fail_silently = False

        my_connection = get_connection(
            host=my_host,
            port=my_port,
            username=my_username,
            password=my_password,
            use_tls=my_use_tls,
            use_ssl=my_use_ssl,
        )

        # Send email with PDF attachment
        email = EmailMessage(
            subject=my_subject,
            body=my_message,
            from_email=my_from_email,
            to=my_recipient_list,
            connection=my_connection,
        )
        email.attach('receipt.pdf', pdf_buffer.getvalue(), 'application/pdf')
        email.send()

        # Optionally, return an HttpResponse or any other response indicating success
        return HttpResponse('Invoice sent successfully.')

    except Exception as e:
        # Handle exceptions appropriately
        print(f"An error occurred while sending the invoice email: {e}")
        return HttpResponse('Failed to send invoice.')


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


