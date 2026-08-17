from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Order, OrderItem, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'product_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = 'Товаров'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'price', 'quantity']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'available', 'image_preview']
    list_filter = ['category', 'available', 'created_at']
    list_editable = ['price', 'stock', 'available']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_select_related = ['category']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: auto; border-radius: 4px;" />',
                obj.image.url,
            )
        return '—'

    image_preview.short_description = 'Фото'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'address', 'total', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    list_editable = ['status']
    search_fields = ['name', 'phone', 'email', 'address']
    inlines = [OrderItemInline]
    readonly_fields = ['name', 'phone', 'email', 'address', 'comment', 'created_at']
    date_hierarchy = 'created_at'

    def total(self, obj):
        return f'{obj.total:,.2f} ₽'.replace(',', ' ')

    total.short_description = 'Сумма'


admin.site.site_header = 'Магазин «Vibe Store» — администрирование'
admin.site.site_title = 'Vibe Store админка'
admin.site.index_title = 'Управление магазином'
