import random
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw, ImageFont

from catalog.models import Category, Product

CATEGORIES = [
    {
        'name': 'Электроника',
        'slug': 'electronics',
        'color': (52, 109, 219),
        'icon': '⚡',
    },
    {
        'name': 'Одежда',
        'slug': 'clothes',
        'color': (219, 68, 96),
        'icon': '👕',
    },
    {
        'name': 'Дом и кухня',
        'slug': 'home',
        'color': (30, 160, 110),
        'icon': '🏠',
    },
]

PRODUCTS = [
    {
        'category': 'electronics', 'name': 'Наушники беспроводные SoundMax Pro',
        'slug': 'headphones-soundmax-pro', 'price': Decimal('4990.00'),
        'stock': 25, 'icon': '🎧',
        'description': 'Беспроводные наушники с активным шумоподавлением, '
                       'запас хода до 30 часов, Bluetooth 5.3 и быстрая зарядка USB-C. '
                       'Комфортные амбушюры из мягкой пены с эффектом памяти.',
    },
    {
        'category': 'electronics', 'name': 'Смарт-часы FitBand X2',
        'slug': 'smartwatch-fitband-x2', 'price': Decimal('7990.00'),
        'stock': 15, 'icon': '⌚',
        'description': 'Умные часы с AMOLED-дисплеем 1.4", мониторингом пульса, '
                       'сна и тренировок. Водозащита 5ATM, до 14 дней автономной работы.',
    },
    {
        'category': 'electronics', 'name': 'Портативная колонка BoomGo',
        'slug': 'speaker-boomgo', 'price': Decimal('3490.00'),
        'stock': 40, 'icon': '🔊',
        'description': 'Компактная Bluetooth-колонка мощностью 20 Вт с глубоким басом. '
                       'Защита от воды IPX7, до 12 часов музыки, можно брать в поездки.',
    },
    {
        'category': 'electronics', 'name': 'Повербанк PowerUp 20000',
        'slug': 'powerbank-powerup-20000', 'price': Decimal('2590.00'),
        'stock': 50, 'icon': '🔋',
        'description': 'Внешний аккумулятор на 20000 мА·ч с двумя USB-портами и '
                       'быстрой зарядкой 22.5 Вт. Хватит на несколько полных зарядов телефона.',
    },
    {
        'category': 'clothes', 'name': 'Худи унисекс Oversize',
        'slug': 'hoodie-oversize', 'price': Decimal('2990.00'),
        'stock': 60, 'icon': '🧥',
        'description': 'Тёплое худи свободного кроя из плотного футера 340 г/м². '
                       'Материал: хлопок 80%, полиэстер 20%. Внутри мягкий начёс.',
    },
    {
        'category': 'clothes', 'name': 'Футболка Classic Cotton',
        'slug': 'tshirt-classic-cotton', 'price': Decimal('990.00'),
        'stock': 100, 'icon': '👕',
        'description': 'Базовая футболка из 100% хлопка плотностью 160 г/м². '
                       'Прямой крой, не вытягивается и не теряет цвет после стирки.',
    },
    {
        'category': 'clothes', 'name': 'Джинсы Slim Fit Denver',
        'slug': 'jeans-slim-denver', 'price': Decimal('3990.00'),
        'stock': 45, 'icon': '👖',
        'description': 'Классические джинсы slim fit из эластичного денима. '
                       'Идеально сидят по фигуре и сохраняют форму весь день.',
    },
    {
        'category': 'clothes', 'name': 'Кроссовки Urban Runner',
        'slug': 'sneakers-urban-runner', 'price': Decimal('5490.00'),
        'stock': 30, 'icon': '👟',
        'description': 'Лёгкие кроссовки с дышащим сетчатым верхом и '
                       'амортизирующей подошвой из EVA. Подойдут и для бега, и для города.',
    },
    {
        'category': 'home', 'name': 'Кофеварка капельная CoffeeTime',
        'slug': 'coffeemaker-coffeetime', 'price': Decimal('4490.00'),
        'stock': 20, 'icon': '☕',
        'description': 'Капельная кофеварка на 1.25 л с функцией подогрева. '
                       'Приготовит до 10 чашек ароматного кофе за 8 минут.',
    },
    {
        'category': 'home', 'name': 'Набор кастрюль Chef 3 шт',
        'slug': 'pots-set-chef', 'price': Decimal('5990.00'),
        'stock': 18, 'icon': '🍲',
        'description': 'Набор кастрюль из нержавеющей стали с многослойным дном. '
                       'Объёмы 2, 3 и 5 литров. Подходят для всех типов плит, включая индукцию.',
    },
    {
        'category': 'home', 'name': 'Светильник LED-панель Лотос',
        'slug': 'lamp-led-lotus', 'price': Decimal('1890.00'),
        'stock': 35, 'icon': '💡',
        'description': 'Настенный LED-светильник с тёплым белым светом и '
                       'сенсорным управлением яркостью. Современный минималистичный дизайн.',
    },
    {
        'category': 'home', 'name': 'Плед плюшевый SoftHome 200x240',
        'slug': 'blanket-softhome', 'price': Decimal('2490.00'),
        'stock': 70, 'icon': '🛋️',
        'description': 'Мягкий плюшевый плед из гипоаллергенного микрофибра. '
                       'Невероятно тёплый и уютный, идеален для вечеров на диване.',
    },
]


class Command(BaseCommand):
    help = 'Заполняет базу демо-данными: категории и товары с изображениями'

    def handle(self, *args, **options):
        self.stdout.write('Генерация данных...')

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('  + суперпользователь: admin / admin123')

        media_dir = Path(settings.MEDIA_ROOT)
        products_dir = media_dir / 'products'
        products_dir.mkdir(parents=True, exist_ok=True)

        try:
            font_path = None
            for candidate in [
                Path(settings.BASE_DIR) / 'static' / 'DejaVuSans.ttf',
                Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),
                Path('C:/Windows/Fonts/arial.ttf'),
            ]:
                if candidate.exists():
                    font_path = str(candidate)
                    break
            font_big = ImageFont.truetype(font_path, 90)
            font_small = ImageFont.truetype(font_path, 36)
        except (OSError, TypeError):
            font_big = ImageFont.load_default()
            font_small = ImageFont.load_default()

        categories = {}
        for cat in CATEGORIES:
            categories[cat['slug']], _ = Category.objects.get_or_create(
                slug=cat['slug'], defaults={'name': cat['name']},
            )
            self.stdout.write(f'  + категория: {cat["name"]}')

        for product_data in PRODUCTS:
            cat = categories[product_data['category']]
            color = next(c for c in CATEGORIES if c['slug'] == cat.slug)['color']

            filename = f"{product_data['slug']}.png"
            filepath = products_dir / filename
            if not filepath.exists():
                self.stdout.write(f'  ~ генерация заглушки: {filename}')
                self._make_image(filepath, color, product_data['icon'], font_big, font_small)

            Product.objects.update_or_create(
                slug=product_data['slug'],
                defaults={
                    'category': cat,
                    'name': product_data['name'],
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'image': f'products/{filename}',
                    'stock': product_data['stock'],
                },
            )
            self.stdout.write(f'  + товар: {product_data["name"]}')

        self.stdout.write(self.style.SUCCESS(f'Готово: {len(PRODUCTS)} товаров, '
                                             f'{len(CATEGORIES)} категории.'))

    def _make_image(self, path, color, icon, font_big, font_small):
        size = (800, 600)
        img = Image.new('RGB', size, color)

        for y in range(size[1]):
            shade = int(35 * (y / size[1]))
            darker = tuple(max(0, c - shade) for c in color)
            for x in range(0, size[0], 8):
                img.paste(darker, (x, y, x + 8, y + 1))

        draw = ImageDraw.Draw(img)
        for _ in range(14):
            x = random.randint(0, size[0])
            y = random.randint(0, size[1])
            r = random.randint(4, 22)
            alpha = random.randint(20, 60)
            c = tuple(min(255, c + 30) for c in color)
            for i in range(r, 0, -1):
                a = alpha * (i / r)
                draw.ellipse((x - i, y - i, x + i, y + i), outline=(c[0], c[1], c[2], int(a)))

        overlay = Image.new('RGBA', size, (255, 255, 255, 0))
        odraw = ImageDraw.Draw(overlay)
        for i in range(0, 90, 6):
            alpha = int(6 * (1 - i / 90))
            odraw.rectangle([(0, i), (size[0], size[1])], fill=(255, 255, 255, alpha))
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(img)

        draw.text((size[0] // 2, size[1] // 2 - 40), icon, font=font_big,
                  anchor='mm', fill=(255, 255, 255, 230))
        draw.text((size[0] // 2, size[1] // 2 + 90), 'VIBE STORE', font=font_small,
                  anchor='mm', fill=(255, 255, 255, 200))
        img.save(path, 'PNG')
