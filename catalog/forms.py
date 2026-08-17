from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'phone', 'email', 'address', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван Иванов'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (900) 000-00-00'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'mail@example.com'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'г. Москва, ул. Примерная, д. 1, кв. 1'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'name': 'Имя',
            'phone': 'Телефон',
            'email': 'Email',
            'address': 'Адрес доставки',
            'comment': 'Комментарий к заказу',
        }
