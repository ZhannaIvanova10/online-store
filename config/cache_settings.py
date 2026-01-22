"""
Настройки кеширования для Django проекта
"""

import os

# Включаем/выключаем кеширование
CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'True') == 'True'

if CACHE_ENABLED:
    # Настройки для Redis
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': 'redis://127.0.0.1:6379/1',
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            },
            'KEY_PREFIX': 'online_store',
        }
    }
else:
    # Локальное кеширование в памяти (для разработки)
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }

# Настройки кеширования представлений
CACHE_MIDDLEWARE_SECONDS = 60 * 15  # 15 минут
CACHE_MIDDLEWARE_KEY_PREFIX = 'online_store'
CACHE_MIDDLEWARE_ALIAS = 'default'
