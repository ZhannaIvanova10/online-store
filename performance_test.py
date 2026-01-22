#!/usr/bin/env python
"""
Нагрузочное тестирование кэширования
"""
import os
import sys
import django
import time
import requests
from concurrent.futures import ThreadPoolExecutor

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

BASE_URL = 'http://127.0.0.1:8000'

def test_single_request():
    """Тестирует один запрос"""
    print("=== ТЕСТ ОДНОГО ЗАПРОСА ===")
    
    start = time.time()
    response = requests.get(BASE_URL + '/')
    end = time.time()
    
    print(f"Время ответа: {(end - start):.4f} секунд")
    print(f"Статус код: {response.status_code}")
    print(f"Размер ответа: {len(response.content)} байт")
    # Проверяем заголовки кэша
    if 'Cache-Control' in response.headers:
        print(f"Cache-Control: {response.headers['Cache-Control']}")
    
    return end - start

def test_multiple_requests(num_requests=10):
    """Тестирует несколько параллельных запросов"""
    print(f"\n=== ТЕСТ {num_requests} ПАРАЛЛЕЛЬНЫХ ЗАПРОСОВ ===")
    
    def make_request(i):
        start = time.time()
        requests.get(BASE_URL + '/')
        end = time.time()
        return end - start
    
    start_total = time.time()
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        times = list(executor.map(make_request, range(num_requests)))
    
    end_total = time.time()
    
    print(f"Общее время: {(end_total - start_total):.4f} секунд")
    print(f"Среднее время запроса: {sum(times)/len(times):.4f} секунд")
    print(f"Максимальное время: {max(times):.4f} секунд")
    print(f"Минимальное время: {min(times):.4f} секунд")
    
    return times

def test_cache_hit_miss():
    """Тестирует попадания и промахи кэша"""
    print("\n=== ТЕСТ ПОПАДАНИЙ/ПРОМАХОВ КЭША ===")
    from django.core.cache import cache
    
    # Очищаем кэш
    cache.clear()
    print("1. Кэш очищен (промах гарантирован)")
    
    # Первый запрос - должен быть промах
    start = time.time()
    requests.get(BASE_URL + '/')
    miss_time = time.time() - start
    print(f"   Время при промахе: {miss_time:.4f}с")
    
    # Второй запрос - должно быть попадание
    start = time.time()
    requests.get(BASE_URL + '/')
    hit_time = time.time() - start
    print(f"2. Второй запрос (должно быть попадание)")
    print(f"   Время при попадании: {hit_time:.4f}с")
    
    print(f"3. Ускорение: {miss_time/hit_time:.2f}x")
    
    return miss_time, hit_time

if __name__ == '__main__':
    print("НАГРУЗОЧНОЕ ТЕСТИРОВАНИЕ КЭШИРОВАНИЯ")
    print("=" * 50)
    
    # Ждем запуска сервера
    print("Убедитесь, что сервер Django запущен на http://127.0.0.1:8000/")
    input("Нажмите Enter когда сервер запущен...")
    # Запускаем тесты
    single_time = test_single_request()
    times = test_multiple_requests(20)
    miss_time, hit_time = test_cache_hit_miss()
    
    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"1. Одиночный запрос: {single_time:.4f}с")
    print(f"2. 20 параллельных запросов: среднее {sum(times)/len(times):.4f}с")
    print(f"3. Промах кэша: {miss_time:.4f}с")
    print(f"4. Попадание в кэш: {hit_time:.4f}с")
    print(f"5. Ускорение от кэширования: {miss_time/hit_time:.2f}x")
    
    if miss_time/hit_time > 1.5:
        print("\n✅ КЭШИРОВАНИЕ РАБОТАЕТ ЭФФЕКТИВНО!")
    else:
        print("\n⚠️  Кэширование дает небольшое ускорение")
        print("   Проверьте настройки cache_page декораторов")
