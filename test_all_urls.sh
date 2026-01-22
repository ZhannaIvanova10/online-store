#!/bin/bash
echo "=== ТЕСТИРОВАНИЕ ВСЕХ URL ==="
echo ""

# Получаем список ID продуктов
IDS=$(py -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from catalog.models import Product
ids = [str(p.id) for p in Product.objects.all()[:3]]
print(' '.join(ids))
" 2>/dev/null)

if [ -z "$IDS" ]; then
    echo "❌ Нет продуктов! Запустите: py create_test_data.py"
    exit 1
fi

echo "Тестируем с продуктами ID: $IDS"
echo ""

# Тестируем каждый URL
for id in $IDS; do
    echo "🔗 Продукт $id:"
    echo -n "  http://localhost:8000/product/$id/ -> "
    curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/product/$id/
    
    echo -n "  http://localhost:8000/category/$id/products/ -> "
    curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/category/$id/products/
    echo ""
done

echo "📊 Другие URL:"
echo -n "  http://localhost:8000/ -> "
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/

echo -n "  http://localhost:8000/category/1/products/ -> "
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/category/1/products/

echo -n "  http://localhost:8000/test-redis/ -> "
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/test-redis/

echo ""
echo "✅ Тестирование завершено!"
