#!/bin/bash
# Деплой Vibe Store на PythonAnywhere
# Выполняется в Bash-консоли PythonAnywhere (по одному блоку)
set -e

# --- Блок 1: клонируем репозиторий ---
cd ~
git clone https://github.com/Flipixxl/vibe-store.git
cd vibe-store

# --- Блок 2: создаём виртуальное окружение ---
# Выберите доступную версию Python: python3.13 или python3.12
python3.13 -m venv venv 2>/dev/null || python3.12 -m venv venv
source venv/bin/activate

# --- Блок 3: зависимости + настройка базы ---
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py collectstatic --noinput

echo ""
echo "ГОТОВО. Дальше настройте веб-приложение во вкладке Web."
echo "Virtualenv: /home/$USER/vibe-store/venv"
