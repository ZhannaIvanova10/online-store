def category_products(request, category_id):
    """
    Представление для отображения продуктов в категории.
    Использует низкоуровневое кэширование через сервисную функцию.
    """
    from .services import get_products_in_category
    
    products = get_products_in_category(category_id)
    
    # Определяем название категории
    if products and hasattr(products[0], 'category') and hasattr(products[0].category, 'name'):
        category_name = products[0].category.name
    elif products and hasattr(products[0], 'categories'):
        # Если ManyToMany связь
        category_name = f"Категория {category_id}"
    else:
        category_name = f"Все продукты (категория {category_id} не найдена)"
    
    context = {
        'products': products,
        'category_id': category_id,
        'category_name': category_name
    }
    
    return render(request, 'catalog/category_products.html', context)
