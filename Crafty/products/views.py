from django.shortcuts import render, get_object_or_404
from .models import Item, Category, SubCategory

def products(request):
    # Get all items or filter by search parameters
    search_query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')

    items = Item.objects.all()

    if search_query:
        items = items.filter(name__icontains=search_query)

    if category_filter:
        items = items.filter(category__name=category_filter)

    categories = Category.objects.all()  # For dropdown filters
    return render(request, 'products/index.html', {'items': items, 'categories': categories})

def product_detail(request, product_id):
    item = get_object_or_404(Item, id=product_id)
    context = {
        'product': item
    }
    return render(request, 'products/product_detail.html', context)

