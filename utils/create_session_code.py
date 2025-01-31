import os
import json
import asyncio
import configparser
import telethon
from telethon import TelegramClient
from telethon.tl.functions.help import GetUserInfoRequest
from pystyle import Write, Colors

async def create_session_code():
    client = None
    try:
        # Чтение конфигурации
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        if 'CODE' not in config or not config['CODE'].get('api_id') or not config['CODE'].get('api_hash') or not config['CODE'].get('device_id'):
            Write.Print("\n    [!] Отсутствуют необходимые параметры в config.ini\n", Colors.red, interval=0.0005)
            Write.Print("    [!] Пожалуйста, настройте API ID/hash и device в меню\n", Colors.red, interval=0.0005)
            return False
            
        api_id = config['CODE']['api_id']
        api_hash = config['CODE']['api_hash']
        device_id = int(config['CODE']['device_id'])

        # Чтение информации об устройстве
        try:
            with open('src/set_apps.json', 'r', encoding='utf-8') as f:
                devices = json.load(f)
                device = devices[device_id]
                device_model = device['device_model']
                system_version = device['system_version']
                app_version = device['app_version']
        except (FileNotFoundError, IndexError, KeyError):
            Write.Print("\n    [!] Ошибка при чтении информации об устройстве\n", Colors.red, interval=0.0005)
            Write.Print("    [!] Проверьте файл set_apps.json и настройки device\n", Colors.red, interval=0.0005)
            return False

        # Создание директории для сессий если её нет
        os.makedirs('results/create_session_code/sessios', exist_ok=True)

        # Удаляем старый файл сессии если существует
        if os.path.exists("results/create_session_code/sessios/temp_session.session"):
            try:
                os.remove("results/create_session_code/sessios/temp_session.session")
            except PermissionError:
                Write.Print("\n    [!] Не удалось удалить старый файл сессии. Возможно, он используется другим процессом.\n", Colors.yellow, interval=0.0005)
                return False

        # Создание клиента
        client = TelegramClient("results/create_session_code/sessios/temp_session",
                              api_id=api_id,
                              api_hash=api_hash,
                              device_model=device_model,
                              system_version=system_version,
                              app_version=app_version)

        await client.connect()

        try:
            # Запрашиваем номер телефона
            Write.Print("\n    Введите номер телефона (в международном формате): ", Colors.cyan, interval=0.0005)
            phone = input()
            
            try:
                await client.send_code_request(phone)
            except telethon.errors.PhoneCodeInvalidError as e:
                Write.Print("\n    [!] Ошибка: Код подтверждения недействителен. Пожалуйста, проверьте введенный номер телефона и попробуйте снова.\n", Colors.red, interval=0.0005)
                Write.Print(f"    [!] Подробности ошибки: {str(e)}\n", Colors.red, interval=0.0005)
                return False
            
            Write.Print("\n    Введите код подтверждения: ", Colors.cyan, interval=0.0005)
            code = input()
            
            try:
                # Пытаемся войти с кодом
                await client.sign_in(phone, code)
            except telethon.errors.SessionPasswordNeededError:
                # Если требуется 2FA
                Write.Print("\n    [!] Требуется двухфакторная аутентификация\n", Colors.yellow, interval=0.0005)
                password = input("    Введите пароль 2FA: ")
                await client.sign_in(password=password)

            if await client.is_user_authorized():
                Write.Print("\n    [+] Успешная авторизация!\n", Colors.cyan_to_blue, interval=0.0005)
                
                # Получаем номер телефона для имени файла
                me = await client.get_me()
                phone = me.phone
                
                # Закрываем соединение перед переименованием
                await client.disconnect()
                
                # Ждем немного, чтобы файл освободился
                await asyncio.sleep(1)
                
                # Переименовываем временный файл сессии
                max_attempts = 3
                for attempt in range(max_attempts):
                    try:
                        os.rename("results/create_session_code/sessios/temp_session.session", f"results/create_session_code/sessios/{phone}.session")
                        Write.Print(f"\n    [+] Файл сессии сохранен как: results/create_session_code/sessios/{phone}.session\n", Colors.cyan_to_blue, interval=0.0005)
                        break
                    except PermissionError:
                        if attempt == max_attempts - 1:
                            Write.Print("\n    [!] Не удалось переименовать файл сессии после нескольких попыток.\n", Colors.yellow, interval=0.0005)
                            return False
                        await asyncio.sleep(1)
                
                return True
            else:
                Write.Print("\n    [!] Не удалось авторизоваться\n", Colors.red, interval=0.0005)
                return False

        except Exception as e:
            Write.Print(f"\n    [!] Ошибка: {str(e)}\n", Colors.red, interval=0.0005)
            return False

    except Exception as e:
        Write.Print(f"\n    [!] Ошибка: {str(e)}\n", Colors.red, interval=0.0005)
        return False
    finally:
        if client and client.is_connected():
            await client.disconnect()