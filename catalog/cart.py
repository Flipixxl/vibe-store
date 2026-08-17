from decimal import Decimal

from django.conf import settings

CART_SESSION_KEY = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if not cart:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def __iter__(self):
        from .models import Product

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['total'] = Decimal(item['price']) * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def update(self, product_id, quantity):
        key = str(product_id)
        if key in self.cart:
            if quantity > 0:
                self.cart[key]['quantity'] = quantity
            else:
                del self.cart[key]
            self.save()

    def remove(self, product_id):
        key = str(product_id)
        if key in self.cart:
            del self.cart[key]
            self.save()

    def clear(self):
        del self.session[CART_SESSION_KEY]
        self.session.modified = True

    def save(self):
        self.session[CART_SESSION_KEY] = self.cart
        self.session.modified = True

    @property
    def total_price(self):
        return sum(Decimal(item['price']) * item['quantity']
                   for item in self.cart.values())

    @property
    def total_quantity(self):
        return sum(item['quantity'] for item in self.cart.values())
