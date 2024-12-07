from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Rating, Item
from django.db.models import Avg, Q

def index(request):
    items = Item.objects.annotate(avg_rating=Avg('rating__stars')).order_by('-avg_rating')
    return render(request, 'ratings/index.html', {'items': items})

@login_required
def rate_item(request):
    if request.method == 'POST' and request.is_ajax():
        item_id = request.POST.get('item_id')
        stars = request.POST.get('stars')
        review = request.POST.get('review', '')
        
        rating, created = Rating.objects.update_or_create(
            user=request.user,
            item_id=item_id,
            defaults={'stars': stars, 'review': review}
        )
        
        # Calculate new average rating
        avg_rating = Rating.objects.filter(item_id=item_id).aggregate(Avg('stars'))['stars__avg']
        
        return JsonResponse({
            'success': True,
            'avg_rating': round(avg_rating, 1) if avg_rating else 0
        })
    return JsonResponse({'success': False})

def get_recommendations(request):
    if not request.user.is_authenticated:
        return JsonResponse({'recommendations': []})
        
    # Get user's highly rated items (4 or 5 stars)
    user_preferences = Rating.objects.filter(
        user=request.user,
        stars__gte=4
    ).values_list('item__category', flat=True)
    
    # Find similar items in the same categories
    recommended_items = Item.objects.filter(
        category__in=user_preferences
    ).exclude(
        rating__user=request.user  # Exclude items user has already rated
    ).annotate(
        avg_rating=Avg('rating__stars')
    ).order_by('-avg_rating')[:5]
    
    return JsonResponse({
        'recommendations': list(recommended_items.values('id', 'name', 'avg_rating'))
    })