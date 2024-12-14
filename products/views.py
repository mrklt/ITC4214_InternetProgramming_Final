from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from .models import Item, Category, SubCategory


def product_list(request):
    items = Item.objects.annotate(avg_rating=Avg('rating__stars'))
    query = request.GET.get('q')
    category = request.GET.get('category')

    if query:
        items = items.filter(name__icontains=query)

    if category:

        try:
            subcategory = SubCategory.objects.get(name=category)
            items = items.filter(subcategory=subcategory)
        except SubCategory.DoesNotExist:

            try:
                category_obj = Category.objects.get(name=category)
                items = items.filter(category=category_obj)
            except Category.DoesNotExist:
                items = items.none()

    context = {
        'items': items,
        'categories': Category.objects.all(),
    }
    return render(request, 'products/index.html', context)

def product_detail(request, product_id):
    item = get_object_or_404(Item, id=product_id)
    context = {
        'product': item
    }
    return render(request, 'products/product_detail.html', context)

