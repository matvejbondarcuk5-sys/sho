from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('favorites/add/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('products/<slug:category_slug>/', views.product_list, name='product_list'),
    path('products/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('register/', views.register, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)