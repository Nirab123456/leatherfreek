from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Display_Product, shopping_cart

@receiver(user_logged_in)
def transfer_session_cart_to_user(sender, request, user, **kwargs):
    if 'cart' in request.session:
        session_cart = request.session['cart']

        for product_id, item in session_cart.items():
            product = Display_Product.objects.get(product_id=product_id)
            
            # Try to get the existing cart item
            try:
                cart_item = shopping_cart.objects.get(user=user, product=product)
                # If it exists, increase the quantity
                cart_item.quantity += item['quantity']
            except shopping_cart.DoesNotExist:
                # If it doesn't exist, create a new cart item
                cart_item = shopping_cart(user=user, product=product, quantity=item['quantity'])
            
            # Save the cart item
            cart_item.save()
        
        # Clear the session cart
        del request.session['cart']
        request.session.modified = True
