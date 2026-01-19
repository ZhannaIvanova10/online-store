from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product

class Command(BaseCommand):
    help = 'Создание групп "Модератор продуктов" и "Контент-менеджер"'
    
    def handle(self, *args, **options):
        self.stdout.write("Создание групп для домашней работы...")
        
        # Получаем ContentType для Product
        product_content_type = ContentType.objects.get_for_model(Product)
        
        # 1. Группа "Модератор продуктов"
        moderator_group, created = Group.objects.get_or_create(
            name='Модератор продуктов'
        )
        if created:
            self.stdout.write('✅ Создана группа "Модератор продуктов"')
        else:
            self.stdout.write('ℹ️  Группа "Модератор продуктов" уже существует')
        
        # Права для модератора продуктов
        moderator_permissions = [
            'delete_product',           # Удаление любого продукта
            'can_unpublish_product',    # Отмена публикации
        ]
        
        for perm_codename in moderator_permissions:
            try:
                perm = Permission.objects.get(
                    content_type=product_content_type,
                    codename=perm_codename
                )
                moderator_group.permissions.add(perm)
                self.stdout.write(f'   ✓ Добавлено право: {perm_codename}')
            except Permission.DoesNotExist:
                self.stdout.write(f'   ✗ Право не найдено: {perm_codename}')
        
        # 2. Группа "Контент-менеджер" (дополнительное задание)
        try:
            # Пробуем найти модель Blog
            from blog.models import Blog
            blog_content_type = ContentType.objects.get_for_model(Blog)
            
            content_group, created = Group.objects.get_or_create(
                name='Контент-менеджер'
            )
            if created:
                self.stdout.write('\n✅ Создана группа "Контент-менеджер"')
            else:
                self.stdout.write('\nℹ️  Группа "Контент-менеджер" уже существует')
            
            # Права для контент-менеджера
            content_permissions = [
                'add_blog',
                'change_blog',
                'delete_blog',
                'view_blog',
            ]
            
            for perm_codename in content_permissions:
                try:
                    perm = Permission.objects.get(
                        content_type=blog_content_type,
                        codename=perm_codename
                    )
                    content_group.permissions.add(perm)
                    self.stdout.write(f'   ✓ Добавлено право: {perm_codename}')
                except Permission.DoesNotExist:
                    self.stdout.write(f'   ⚠️  Право не найдено: {perm_codename}')
                    
        except ImportError:
            self.stdout.write('\n⚠️  Приложение blog не найдено, пропускаем создание группы "Контент-менеджер"')
        
        self.stdout.write(
            self.style.SUCCESS('\n✅ Группы успешно настроены!')
        )
