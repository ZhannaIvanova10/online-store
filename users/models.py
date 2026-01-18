from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Менеджер для модели User без поля username"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Создает и возвращает пользователя с email и паролем"""
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        """Создает и возвращает суперпользователя"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Кастомная модель пользователя"""
    username = None  # Убираем поле username
    
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("Пользователь с таким email уже существует."),
        }
    )
    
    avatar = models.ImageField(
        _('аватар'),
        upload_to='users/avatars/',
        blank=True,
        null=True,
    )
    phone = models.CharField(
        _('номер телефона'),
        max_length=20,
        blank=True,
    )
    
    country = models.CharField(
        _('страна'),
        max_length=100,
        blank=True,
    )
    
    USERNAME_FIELD = 'email'  # Поле для авторизации
    REQUIRED_FIELDS = []  # Обязательные поля при создании суперпользователя
    
    objects = UserManager()  # Используем кастомный менеджер
    
    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.email

    def get_full_name(self):
        """Возвращает полное имя пользователя"""
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name if full_name else self.email
    
    def get_short_name(self):
        """Возвращает короткое имя пользователя"""
        return self.first_name or self.email.split('@')[0]
