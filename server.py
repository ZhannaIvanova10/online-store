"""
Простой HTTP сервер для ДЗ 1.
Возвращает страницу контактов на любой GET запрос.
"""
import http.server
import socketserver
import sys
class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Кастомный обработчик HTTP запросов."""
    
    def do_GET(self):
        """Обработка GET запросов."""
        try:
            # Читаем файл contacts.html
            with open('templates/contacts.html', 'r', encoding='utf-8') as file:
                html_content = file.read()
            
            # Отправляем успешный ответ
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # Отправляем HTML контент
            self.wfile.write(html_content.encode('utf-8'))
            
            # Логируем запрос
            print(f"GET запрос получен от {self.client_address[0]}")
        except FileNotFoundError:
            # Если файл не найден
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("Ошибка 404: Файл не найден".encode('utf-8'))
    
    def do_POST(self):
        """Обработка POST запросов (дополнительное задание)."""
        # Получаем длину содержимого
        content_length = int(self.headers.get('Content-Length', 0))
        
        # Читаем данные
        post_data = self.rfile.read(content_length)
        
        # Декодируем данные
        try:
            decoded_data = post_data.decode('utf-8')
        except UnicodeDecodeError:
            decoded_data = str(post_data)
        # Выводим данные в консоль
        print("\n" + "="*50)
        print("ПОЛУЧЕНЫ POST ДАННЫЕ:")
        print(f"Заголовки: {dict(self.headers)}")
        print(f"Данные: {decoded_data}")
        print("="*50 + "\n")
        
        # Отправляем ответ
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write("POST данные получены и выведены в консоль".encode('utf-8'))

def run_server(port=8000):
    """Запуск сервера."""
    try:
        with socketserver.TCPServer(("", port), SimpleHTTPRequestHandler) as httpd:
            print(f"Сервер запущен на порту {port}")
            print(f"Откройте в браузере: http://localhost:{port}")
            print("Нажмите Ctrl+C для остановки сервера\n")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
        sys.exit(0)
    except OSError as e:
        if e.errno == 10048:  # Порт занят
            print(f"Ошибка: Порт {port} уже занят")
            print("Попробуйте другой порт: python server.py 8080")
            sys.exit(1)
        else:
            raise

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Запуск простого HTTP сервера')
    parser.add_argument('--port', '-p', type=int, default=8000,
                       help='Порт для запуска сервера (по умолчанию: 8000)')
    
    args = parser.parse_args()
    run_server(args.port)
