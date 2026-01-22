# Домашняя работа: Кэширование с Redis в Django

## 🎯 Цель
Настроить кэширование страниц и данных в Django проекте с использованием Redis.

## ✅ Выполненные задачи

### 1. Установка и настройка Redis
- Установлен Redis сервер (порт 6379)
- Настроено подключение Django к Redis
- Проверена работа соединения

### 2. Настройка Django для кэширования
В `config/settings.py` добавлены:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
