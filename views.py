from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, STATUS_ACTIVE, Favorite

def product_list(request, category_slug=None):
    products = Product.objects.filter(status=STATUS_ACTIVE)
    category = None
    search_query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'name')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if search_query:
        products = products.filter(name__icontains=search_query)

    if sort_by == 'price':
        products = products.order_by('price')
    elif sort_by == '-price':
        products = products.order_by('-price')
    elif sort_by == 'created':
        products = products.order_by('-created')
    else:
        products = products.order_by('name')

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    categories = Category.objects.all()
    return render(request, 'main/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products_page,
        'search_query': search_query,
        'sort_by': sort_by,
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, status=STATUS_ACTIVE)
    related_products = Product.objects.filter(
        category=product.category,
        status=STATUS_ACTIVE
    ).exclude(id=product.id)[:4]
    return render(request, 'main/product/detail.html', {
        'product': product,
        'related_products': related_products,
    })

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'main/favorites.html', {'favorites': favorites})

@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id, status=STATUS_ACTIVE)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, f'Трек "{product.name}" добавлен в избранное')
    else:
        messages.info(request, f'Трек "{product.name}" уже в избранном')
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))