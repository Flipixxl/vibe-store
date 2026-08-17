# Vibe Store — интернет-магазин на Django

Портфолио-проект: полноценный интернет-магазин на Django с корзиной на
сессиях, оформлением заказов и админ-панелью.

## Возможности

- **Каталог товаров** — категории, фильтр по цене, сортировка, поиск по названию
- **Карточка товара** — фото, описание, цена, похожие товары
- **Корзина на сессиях** — добавить / удалить / изменить количество
- **Оформление заказа** — форма (имя, телефон, адрес) → сохранение в БД
- **Админ-панель** — управление товарами, категориями, статусами заказов
- **Страницы** — главная, каталог, товар, корзина, оформление, «О нас», «Контакты»
- **Адаптивная вёрстка** — Bootstrap 5, корректно на мобильных

## Стек

Python 3.13 · Django 6.1 · SQLite · HTML/CSS/JS · Bootstrap 5 · Pillow

## Установка и запуск

```bash
# 1. Создать виртуальное окружение
python -m venv .venv

# 2. Активировать (Windows)
.venv\Scripts\activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Применить миграции
python manage.py migrate

# 5. Заполнить базу демо-данными
python manage.py seed_data

# 6. Создать суперпользователя для админки
python manage.py createsuperuser

# 7. Запустить сервер
python manage.py runserver
```

Дальше откройте:

- **Магазин:** http://127.0.0.1:8000/
- **Админка:** http://127.0.0.1:8000/admin/ (admin / admin123, создаётся командой seed_data при первом запуске)

## Структура проекта

```
shop/
├── config/            # настройки проекта (settings, urls, wsgi/asgi)
├── catalog/           # основное приложение
│   ├── models.py      # Category, Product, Order, OrderItem
│   ├── views.py       # все страницы и обработчики корзины
│   ├── cart.py        # логика корзины на сессиях
│   ├── forms.py       # форма заказа
│   ├── admin.py       # настройка админ-панели
│   ├── context_processors.py  # счётчик и сумма корзины в шаблоне
│   ├── urls.py        # маршруты магазина
│   └── management/commands/seed_data.py  # генерация демо-данных
├── static/            # CSS (Bootstrap + кастомные стили)
├── media/products/    # сгенерированные изображения товаров
├── manage.py
└── requirements.txt
```

## Модели данных

| Модель      | Поля (ключевые)                                              |
|-------------|---------------------------------------------------------------|
| Category    | name, slug                                                    |
| Product     | category (FK), name, slug, description, price, image, stock   |
| Order       | name, phone, email, address, comment, status                  |
| OrderItem   | order (FK), product (FK), price, quantity                     |

## Демо-данные

Команда `python manage.py seed_data` создаёт:

- 3 категории: Электроника, Одежда, Дом и кухня
- 12 товаров с описаниями и сгенерированными изображениями
- Суперпользователя `admin` / `admin123` (только при первой загрузке пустой БД)

## Скриншоты для портфолио

1. **Главная** — `/` — hero-блок, категории, хиты продаж
2. **Каталог с фильтрами** — `/catalog/` — панель фильтров слева, сортировка
3. **Карточка товара** — `/product/headphones-soundmax-pro/`
4. **Корзина** — `/cart/`
5. **Оформление** — `/checkout/`
6. **Страница успеха** — `/order/1/success/`
7. **Админка** — `/admin/` — список заказов со статусами, inline-позиции

Для полного цикла: добавьте товар в корзину → оформите заказ → откройте
админку и поменяйте статус заказа.

## Деплой на Render (бесплатно, деплой в один клик)

Репозиторий содержит `render.yaml` — развёртывание через Blueprint:

1. Зарегистрируйтесь на [render.com](https://render.com) (лучше войти через GitHub)
2. Нажмите **New +** → **Blueprint**
3. Подключите репозиторий **vibe-store** и нажмите **Apply**
4. Render сам запустит миграции, сгенерирует демо-данные (включая изображения)
   и поднимет сайт на **https://vibe-store.onrender.com** (~3 минуты)

Админка: **https://vibe-store.onrender.com/admin/** (логин `admin`, пароль `admin123`).

Полезные переменные окружения (уже заданы в `render.yaml`):

| Переменная            | Назначение                          |
|-----------------------|-------------------------------------|
| `DJANGO_SECRET_KEY`   | секретный ключ (генерируется автоматически) |
| `DJANGO_DEBUG`        | `False` в проде                     |
| `DJANGO_ALLOWED_HOSTS`| домены сайта через запятую          |

Данные хранятся в SQLite на эфемерном диске Render — при каждом деплое база
пересоздаётся из демо-данных (для портфолио это плюс: заказы не засоряются).
Для продакшена подключите PostgreSQL через Render.

### Альтернатива: PythonAnywhere (доступно из РФ)

### Шаг 1. Регистрация
1. Зарегистрируйтесь на [pythonanywhere.com](https://www.pythonanywhere.com) — бесплатный тариф Beginner
2. Подтвердите email

### Шаг 2. Установка кода (Bash-консоль)
В правом верхнем углу: **Consoles** → **Bash**. Вставьте команды из
`deploy_pythonanywhere.sh` (или вручную):

```bash
cd ~
git clone https://github.com/Flipixxl/vibe-store.git
cd vibe-store
python3.13 -m venv venv 2>/dev/null || python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py collectstatic --noinput
```

### Шаг 3. Создание веб-приложения
Вкладка **Web** → **Add a new web app**:
1. **Manual configuration** → Python 3.13 (или 3.12)
2. В разделе **Virtualenv**: укажите путь
   `/home/<ВАШ_ЛОГИН>/vibe-store/venv` и нажмите кнопку
   «Enter path… / click to set»
3. В разделе **Code**: откройте WSGI-файл и замените содержимое на:

```python
import os
import sys

sys.path.insert(0, '/home/<ВАШ_ЛОГИН>/vibe-store')

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

4. В разделе **Environment variables** добавьте:

| Имя                   | Значение                                    |
|-----------------------|---------------------------------------------|
| `DJANGO_DEBUG`        | `False`                                     |
| `DJANGO_ALLOWED_HOSTS`| `<ВАШ_ЛОГИН>.pythonanywhere.com`            |
| `DJANGO_SECRET_KEY`   | любой длинный случайный набор символов      |

5. Нажмите **Reload** (зелёная кнопка сверху)

Готово! Сайт будет доступен по адресу:
**https://<ВАШ_ЛОГИН>.pythonanywhere.com** (админка `/admin/`, логин `admin`,
пароль `admin123`).

> Статические файлы и картинки раздаёт сам Django через WhiteNoise —
> дополнительные настройки статики во вкладке Web не нужны.


