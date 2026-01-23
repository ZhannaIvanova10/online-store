import os

settings_path = 'config/settings.py'
if os.path.exists(settings_path):
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print("🔍 Поиск настроек Redis в settings.py:")
    print("=" * 50)

    # Ищем CACHES
    if 'CACHES' in content:
        print("✅ Настройки CACHES найдены")

        # Извлекаем блок CACHES
        import re
        cache_match = re.search(r'CACHES\s*=\s*\{[^}]+\}', content, re.DOTALL)
        if cache_match:
            print("\n📋 Текущие настройки кеша:")
            print(cache_match.group(0))
    else:
        print("❌ Настройки CACHES не найдены")
        print("\n📋 Добавьте в конец settings.py следующий код:")
        print('''
# Настройки Redis для кеширования
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',  # Используем БД #1
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'onlinestore',
    }
}
🔧 Проверяем настройки Redis в settings.py...
> # Время кеширования для middleware (если используется)
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 60 * 15  # 15 минут
CACHE_MIDDLEWARE_KEY_PREFIX = 'onlinestore'
''')

    print("\n" + "=" * 50)

except Exception as e:
    print(f"Ошибка: {e}")
