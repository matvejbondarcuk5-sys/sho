from django.contrib import admin
from .models import Category, Product



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display        = ['name', 'category', 'price', 'status', 'created', 'updated']
    list_filter         = ['category', 'status', 'created', 'updated']
    list_editable       = ['price', 'status']
    prepopulated_fields = {'slug': ('name',)}