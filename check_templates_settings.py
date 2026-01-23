import os

settings_path = 'config/settings.py'
if os.path.exists(settings_path):
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔍 Настройки TEMPLATES в settings.py:")
    print("=" * 60)
    
    # Ищем блок TEMPLATES
    import re
    templates_match = re.search(r'TEMPLATES\s*=\s*\[[^]]+\]', content, re.DOTALL)
    if templates_match:
        templates_config = templates_match.group(0)
        print(templates_config[:500] + "..." if len(templates_config) > 500 else templates_config)
        
        # Проверяем DIRS
        if 'DIRS' in templates_config:
            print("\n✅ TEMPLATES['DIRS'] настроен")
            if 'BASE_DIR' in templates_config and 'templates' in templates_config:
                print("   Используются шаблоны из templates/")
            else:
                print("   DIRS настроен иначе")
        else:
            print("\n❌ TEMPLATES['DIRS'] не настроен")
            
        # Проверяем APP_DIRS
        if "'APP_DIRS': True" in templates_config:
            print("✅ APP_DIRS: True (шаблоны из catalog/templates/)")
        else:
            print("❌ APP_DIRS: False")
    else:
        print("❌ Блок TEMPLATES не найден")
    
    print("\n" + "=" * 60)
