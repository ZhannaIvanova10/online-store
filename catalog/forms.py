from django import forms
from django.core.exceptions import ValidationError
from .models import Product


FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа', 
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Стилизация всех полей
        for field_name, field in self.fields.items():
            if field_name not in ['is_published']:
                if not field.widget.attrs.get('class'):
                    field.widget.attrs['class'] = 'form-control'
        # Специальная стилизация для checkbox
        self.fields['is_published'].widget.attrs['class'] = 'form-check-input'
    
    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        for word in FORBIDDEN_WORDS:
            if word in name:
                raise ValidationError(f'Название содержит запрещенное слово: "{word}"')
        return self.cleaned_data['name']
    
    def clean_description(self):
        description = self.cleaned_data['description'].lower()
        for word in FORBIDDEN_WORDS:
            if word in description:
                raise ValidationError(f'Описание содержит запрещенное слово: "{word}"')
        return self.cleaned_data['description']
    
    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        return price
