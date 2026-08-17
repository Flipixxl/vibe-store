from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .cart import Cart
from .forms import OrderForm
from .models import Category, Order, OrderItem, Product


def home(request):
    categories = Category.objects.all()
    featured = Product.objects.filter(available=True)[:4]
    return render(request, 'catalog/home.html', {
        'categories': categories,
        'featured': featured,
    })


def catalog(request):
    products = Product.objects.filter(available=True).select_related('category')

    category_slug = request.GET.get('category')
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    sort = request.GET.get('sort', '')
    sort_map = {
        'price_asc': 'price',
        'price_desc': '-price',
        'name': 'name',
        'new': '-created_at',
    }
    if sort in sort_map:
        products = products.order_by(sort_map[sort])

    categories = Category.objects.all()
    return render(request, 'catalog/catalog.html', {
        'products': products,
        'categories': categories,
        'current_category': category,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'sort': sort,
    })


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category'), slug=slug,
    )
    related = Product.objects.filter(
        category=product.category, available=True,
    ).exclude(id=product.id)[:4]
    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'related': related,
    })


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'catalog/cart.html', {'cart': cart})


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    cart = Cart(request)
    cart.add(product)
    messages.success(request, f'«{product.name}» добавлен в корзину')
    return redirect(request.META.get('HTTP_REFERER') or 'catalog:cart')


def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('catalog:cart')


def cart_update(request, product_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            quantity = 0
        cart = Cart(request)
        cart.update(product_id, quantity)
    return redirect('catalog:cart')


def checkout(request):
    cart = Cart(request)
    if not cart:
        return redirect('catalog:cart')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            cart.clear()
            messages.success(request, f'Заказ #{order.pk} успешно оформлен!')
            return redirect('catalog:order_success', order_pk=order.pk)
    else:
        form = OrderForm()

    return render(request, 'catalog/checkout.html', {
        'form': form,
        'cart': cart,
    })


def order_success(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    return render(request, 'catalog/order_success.html', {'order': order})


def about(request):
    return render(request, 'catalog/about.html')


def contacts(request):
    return render(request, 'catalog/contacts.html')
