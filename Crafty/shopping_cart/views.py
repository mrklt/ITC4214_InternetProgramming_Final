from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Item
from .models import CartItem


def shopping_cart(request):
    return render(request, 'shopping_cart/index.html')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Item, id=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        # Check if item already exists in cart
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Update quantity if item already exists
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, f'Added {quantity} {product.name} to your cart.')
        return redirect('cart_view')

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in cart_items)
    return render(request, 'shopping_cart/cart.html', {
        'cart_items': cart_items,
        'total': total
    })
