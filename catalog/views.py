from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages

class HomeView(TemplateView):
    """Контроллер для главной страницы."""
    template_name = 'catalog/home.html'

class ContactsView(TemplateView):
    """Контроллер для страницы контактов."""
    template_name = 'catalog/contacts.html'
    
    def post(self, request, *args, **kwargs):
        """Обработка POST запроса из формы контактов."""
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        # В реальном проекте здесь была бы отправка email или сохранение в БД
        print(f"Получено сообщение от {name} ({email}): {message}")
        
        # Добавляем сообщение об успехе
        messages.success(request, 'Сообщение успешно отправлено!')
        
        return render(request, self.template_name)
