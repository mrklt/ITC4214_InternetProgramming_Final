from django.contrib import admin
from .models import Category, SubCategory, Item
from ratings.models import Rating

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0
    readonly_fields = ('user', 'stars', 'created_at')
    can_delete = False

class ProductAdmin(admin.ModelAdmin):
    inlines = [RatingInline]

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Item, ProductAdmin)

