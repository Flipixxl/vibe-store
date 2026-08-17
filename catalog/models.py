from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('Слаг', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:catalog') + f'?category={self.slug}'


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Категория',
        related_name='products',
    )
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('Слаг', max_length=200, unique=True)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена, ₽', max_digits=10, decimal_places=2)
    image = models.ImageField('Фото', upload_to='products/', blank=True)
    stock = models.PositiveIntegerField('В наличии', default=0)
    available = models.BooleanField('Доступен', default=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email', blank=True)
    address = models.CharField('Адрес', max_length=300)
    comment = models.TextField('Комментарий', blank=True)
    status = models.CharField(
        'Статус', max_length=20, choices=STATUS_CHOICES, default='new',
    )
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.pk} — {self.name}'

    @property
    def total(self):
        return sum(item.total for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name='Заказ',
        related_name='items',
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, verbose_name='Товар',
        related_name='order_items', null=True,
    )
    price = models.DecimalField('Цена за единицу, ₽', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество', default=1)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f'{self.quantity} × {self.product}'

    @property
    def total(self):
        return self.price * self.quantity
