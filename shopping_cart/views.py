from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from products.models import Item
from .models import CartItem
from ratings.views import get_recommendations 
from products.views import product_detail 
import json

def add_to_cart(request, product_id):
    product = get_object_or_404(Item, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        messages.success(request, f'Added {quantity} {product.name} to your cart.')
        return redirect('shopping_cart')
    else:

        request.session['pending_cart_item'] = {'product_id': product.id, 'quantity': quantity}
        messages.info(request, 'Please log in to add items to your cart.')
        return redirect('login')


@login_required
def shopping_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.get_total() for item in cart_items)

    recommendations = []
    if request.user.is_authenticated:
        recommendations_response = get_recommendations(request)
        recommendations = json.loads(recommendations_response.content).get('recommendations', [])

    print("Recommendations:", recommendations)

    context = {
        'cart_items': cart_items,
        'total': total,
        'recommendations': recommendations
    }
    return render(request, 'shopping_cart/index.html', context)


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if request.method == 'POST':
        product_name = cart_item.product.name
        cart_item.delete()
        messages.success(request, f'Removed {product_name} from your cart.')
    return redirect('shopping_cart')
