from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import shopping_cart, Display_Product
from django.shortcuts import render , get_object_or_404

@login_required
@require_POST
def add_to_cart_ajax(request, product_id):
    print(product_id)
    product_name = product_id
    product = get_object_or_404(Display_Product, product_id=product_id)
    #check if exist increase quantity by 1
    cart_item = shopping_cart.objects.filter(user=request.user, product=product).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        shopping_cart.objects.create(user=request.user, product=product, quantity=1)
    return JsonResponse({'success': True , 'product': product.product_name})


def increase_quantity_ajax(request, product_id):
    product = get_object_or_404(Display_Product, product_id=product_id)
    cart_item = shopping_cart.objects.filter(user=request.user, product=product).first()
    cart_item.quantity += 1
    cart_item.save()
    return JsonResponse({'success': True, 'product': product.product_name})

def decrease_quantity_ajax(request, product_id):
    product = get_object_or_404(Display_Product, product_id=product_id)
    cart_item = shopping_cart.objects.filter(user=request.user, product=product).first()
    cart_item.quantity -= 1
    cart_item.save()
    return JsonResponse({'success': True, 'product': product.product_name})

def remove_from_cart_ajax(request, product_id):
    product = get_object_or_404(Display_Product, product_id=product_id)
    cart_item = shopping_cart.objects.filter(user=request.user, product=product).first()
    cart_item.delete()
    return JsonResponse({'success': True, 'product': product.product_name})