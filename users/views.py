from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm
from .models import User
class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Отправка приветственного письма
        user_email = form.cleaned_data.get('email')
        subject = 'Добро пожаловать в наш онлайн-магазин!'
        message = '''Здравствуйте!

Благодарим вас за регистрацию в нашем онлайн-магазине.
Теперь вы можете:
- Просматривать каталог товаров
- Создавать и редактировать свои товары
- Управлять своим профилем

С уважением,
Команда онлайн-магазина'''
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[user_email],
                fail_silently=False,
            )
            messages.success(
                self.request,
                'Регистрация прошла успешно! На вашу почту отправлено приветственное письмо.'
            )
        except Exception:
            messages.success(
                self.request,
                'Регистрация прошла успешно! Не удалось отправить приветственное письмо.'
            )
        
        return response

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        messages.success(self.request, 'Вы успешно авторизовались!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка авторизации. Проверьте email и пароль.')
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Вы вышли из системы.')
        return super().dispatch(request, *args, **kwargs)


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)
