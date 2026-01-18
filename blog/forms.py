from django import forms
from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    """Форма для создания и редактирования блоговой записи."""
    
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'preview', 'is_published', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок статьи'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Введите текст статьи'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'my-awesome-post'
            }),
        }
