import os
import json
import qrcode
import asyncio
import configparser
import telethon
from telethon import TelegramClient
from telethon.tl.functions.help import GetUserInfoRequest
from pystyle import Write, Colors

def gen_qr(token: str) -> str:
    """Генерирует и возвращает токен QR-кода"""
    return token

async def create_session_qr():
    client = None
    try:
        # Чтение конфигурации
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        if 'QR' not in config or not config['QR'].get('api_id') or not config['QR'].get('api_hash') or not config['QR'].get('device_id'):
            Write.Print("\n    [!] Отсутствуют необходимые параметры в config.ini\n", Colors.red, interval=0.0005)
            Write.Print("    [!] Пожалуйста, настройте API ID/hash и device в меню\n", Colors.red, interval=0.0005)
            return False
            
        api_id = int(str(config['QR']['api_id']).strip())
        api_hash = str(config['QR']['api_hash']).strip()
        device_id = int(config['QR']['device_id'])

        # Новая проверка длины API hash
        if len(api_hash) != 32:
            Write.Print("\n    [!] Неверная длина API hash (должно быть 32 символа)\n", Colors.red, interval=0.0005)
            return False

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
        os.makedirs('results/create_session_qrcode/sessios', exist_ok=True)

        # Удаляем старый файл сессии если существует
        if os.path.exists("results/create_session_qrcode/sessios/temp_session.session"):
            try:
                os.remove("results/create_session_qrcode/sessios/temp_session.session")
            except PermissionError:
                Write.Print("\n    [!] Не удалось удалить старый файл сессии. Возможно, он используется другим процессом.\n", Colors.yellow, interval=0.0005)
                return False

        # Создание клиента
        client = TelegramClient(
            "results/create_session_qrcode/sessios/temp_session", 
            api_id=api_id,
            api_hash=api_hash,
            device_model=device_model,
            system_version=system_version,
            app_version=app_version
        )

        await client.connect()

        try:
            qr_login = await client.qr_login()
            qr_token = gen_qr(qr_login.url)
            
            # Создание QR кода
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_token)
            qr.make(fit=True)
            
            # Вывод QR кода
            Write.Print("\n    Отсканируйте этот QR код в приложении Telegram:\n", Colors.cyan, interval=0.0005)
            qr.print_ascii()
            
            Write.Print("\n    Ожидание сканирования QR кода...\n", Colors.blue_to_cyan, interval=0.0005)
            Write.Print("    Нажмите Enter для отмены\n", Colors.blue_to_cyan, interval=0.0005)

            # Создаем задачу для ожидания QR логина
            login_task = asyncio.create_task(qr_login.wait(timeout=120))
            
            # Создаем задачу для ожидания нажатия Enter
            async def wait_enter():
                await asyncio.get_event_loop().run_in_executor(None, input)
                return True

            enter_task = asyncio.create_task(wait_enter())
            
            # Ждем что произойдет первым - сканирование QR или нажатие Enter
            done, pending = await asyncio.wait(
                [login_task, enter_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Отменяем оставшуюся задачу
            for task in pending:
                task.cancel()
                
            # Если нажали Enter - возвращаемся в меню
            if enter_task in done:
                Write.Print("\n    [!] Отменено пользователем\n", Colors.yellow, interval=0.0005)
                return False

            if await client.is_user_authorized():
                Write.Print("\n    [+] Успешная авторизация!\n", Colors.cyan_to_blue, interval=0.0005)
                
                # Получаем номер телефона
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
                        os.rename("results/create_session_qrcode/sessios/temp_session.session", f"results/create_session_qrcode/sessios/{phone}.session")
                        Write.Print(f"\n    [+] Файл сессии сохранен как: results/create_session_qrcode/sessios/{phone}.session\n", Colors.cyan_to_blue, interval=0.0005)
                        break
                    except PermissionError:
                        if attempt == max_attempts - 1:
                            Write.Print("\n    [!] Не удалось переименовать файл сессии после нескольких попыток.\n", Colors.yellow, interval=0.0005)
                            return False
                        await asyncio.sleep(1)
                
                return True
            else:
                # Если требуется 2FA
                Write.Print("\n    [!] Требуется двухфакторная аутентификация\n", Colors.yellow, interval=0.0005)
                try:
                    password = input("    Введите пароль 2FA: ")
                    await client.sign_in(password=password)
                    Write.Print("\n    [+] Успешная авторизация с 2FA!\n", Colors.cyan_to_blue, interval=0.0005)
                    
                    me = await client.get_me()
                    phone = me.phone
                    
                    # Закрываем соединение перед переименованием
                    await client.disconnect()
                    
                    # Ждем немного, чтобы файл освободился
                    await asyncio.sleep(1)
                    
                    # Переименовываем с несколькими попытками
                    max_attempts = 3
                    for attempt in range(max_attempts):
                        try:
                            os.rename("results/create_session_qrcode/sessios/temp_session.session", f"results/create_session_qrcode/sessios/{phone}.session")
                            Write.Print(f"\n    [+] Файл сессии сохранен как: results/create_session_qrcode/sessios/{phone}.session\n", Colors.cyan_to_blue, interval=0.0005)
                            break
                        except PermissionError:
                            if attempt == max_attempts - 1:
                                Write.Print("\n    [!] Не удалось переименовать файл сессии после нескольких попыток.\n", Colors.yellow, interval=0.0005)
                                return False
                            await asyncio.sleep(1)
                    
                    return True
                except Exception as e:
                    Write.Print(f"\n    [!] Ошибка при вводе пароля 2FA: {str(e)}\n", Colors.red, interval=0.0005)
                    return False

        except telethon.errors.rpcerrorlist.SessionPasswordNeededError:
            Write.Print("\n    [!] Требуется пароль 2FA\n", Colors.yellow, interval=0.0005)
            try:
                password = input("    Введите пароль 2FA: ")
                await client.sign_in(password=password)
                Write.Print("\n    [+] Успешная авторизация с 2FA!\n", Colors.cyan_to_blue, interval=0.0005)
                
                me = await client.get_me()
                phone = me.phone
                
                # Закрываем соединение перед переименованием
                await client.disconnect()
                
                # Ждем немного, чтобы файл освободился
                await asyncio.sleep(1)
                
                # Переименовываем с несколькими попытками
                max_attempts = 3
                for attempt in range(max_attempts):
                    try:
                        os.rename("results/create_session_qrcode/sessios/temp_session.session", f"results/create_session_qrcode/sessios/{phone}.session")
                        Write.Print(f"\n    [+] Файл сессии сохранен как: results/create_session_qrcode/sessios/{phone}.session\n", Colors.cyan_to_blue, interval=0.0005)
                        break
                    except PermissionError:
                        if attempt == max_attempts - 1:
                            Write.Print("\n    [!] Не удалось переименовать файл сессии после нескольких попыток.\n", Colors.yellow, interval=0.0005)
                            return False
                        await asyncio.sleep(1)
                
                return True
            except Exception as e:
                Write.Print(f"\n    [!] Ошибка при вводе пароля 2FA: {str(e)}\n", Colors.red, interval=0.0005)
                return False

    except Exception as e:
        Write.Print(f"\n    [!] Ошибка: {str(e)}\n", Colors.red, interval=0.0005)
        return False
    finally:
        if client and client.is_connected():
            await client.disconnect()