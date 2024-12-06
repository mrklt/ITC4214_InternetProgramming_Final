from django.contrib import admin
from .models import Rating

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'stars', 'created_at')
    list_filter = ('stars', 'created_at')
    search_fields = ('user__username', 'item__name')
