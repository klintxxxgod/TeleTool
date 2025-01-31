import os
import logging
import configparser
import random
import json
from pathlib import Path
from telethon.sync import TelegramClient
from telethon.tl.types import User, Chat, Channel
from pystyle import Write, Colors

# Настраиваем логирование
logging.basicConfig(
    filename='results/cleaner/cleaner.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

def get_random_session():
    """Находит случайный .session файл в папке results/cleaner/sessions"""
    sessions_dir = Path('results/cleaner/sessions')
    sessions_dir.mkdir(parents=True, exist_ok=True)
    
    session_files = list(sessions_dir.glob('*.session'))
    if not session_files:
        return None
    return random.choice(session_files)

async def count_dialogs(dialog_type):
    """
    Подсчитывает количество диалогов определенного типа
    dialog_type может быть: 'user', 'chat', 'channel', 'bot'
    """
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        if 'DLG' not in config or not config['DLG'].get('api_id') or not config['DLG'].get('api_hash') or not config['DLG'].get('device_id'):
            Write.Print("\n    [!] Отсутствуют необходимые параметры в config.ini\n", Colors.red, interval=0.0005)
            return False
            
        api_id = config['DLG']['api_id']
        api_hash = config['DLG']['api_hash']
        device_id = int(config['DLG']['device_id'])

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
            return False

        # Получаем случайную сессию
        session_file = get_random_session()
        if not session_file:
            Write.Print("\n    [!] Не найдены .session файлы в папке results/cleaner/sessions\n", Colors.red, interval=0.0005)
            return False

        # Создаем клиент
        client = TelegramClient(str(session_file), api_id, api_hash,
                              device_model=device_model,
                              system_version=system_version,
                              app_version=app_version)
        await client.connect()

        if not await client.is_user_authorized():
            Write.Print("\n    [!] Сессия не авторизована\n", Colors.red, interval=0.0005)
            return False

        count = 0
        async for dialog in client.iter_dialogs():
            entity = dialog.entity
            
            if dialog_type == 'user' and isinstance(entity, User) and not entity.bot:
                count += 1
            elif dialog_type == 'chat' and isinstance(entity, Chat):
                count += 1
            elif dialog_type == 'channel' and isinstance(entity, Channel) and not entity.megagroup:
                count += 1
            elif dialog_type == 'bot' and isinstance(entity, User) and entity.bot:
                count += 1

        Write.Print(f"\n    [+] Найдено {count} {dialog_type}(ов)\n", Colors.cyan_to_blue, interval=0.0005)
        logging.info(f"Подсчитано {count} {dialog_type}(ов)")
        return count

    except Exception as e:
        logging.error(f"Ошибка при подсчете диалогов: {e}")
        Write.Print(f"\n    [!] Ошибка: {str(e)}\n", Colors.red, interval=0.0005)
        return False

    finally:
        if 'client' in locals():
            await client.disconnect()

async def clean_dialogs(dialog_type):
    """
    Удаляет/выходит из всех диалогов определенного типа
    dialog_type может быть: 'user', 'chat', 'channel', 'bot'
    """
    try:
        # Читаем конфиг
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        if 'DLG' not in config or not config['DLG'].get('api_id') or not config['DLG'].get('api_hash') or not config['DLG'].get('device_id'):
            Write.Print("\n    [!] Отсутствуют API параметры в config.ini\n", Colors.red, interval=0.0005)
            return False
            
        api_id = config['DLG']['api_id']
        api_hash = config['DLG']['api_hash']
        device_id = int(config['DLG']['device_id'])

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
            return False

        # Получаем случайную сессию
        session_file = get_random_session()
        if not session_file:
            Write.Print("\n    [!] Не найдены .session файлы в папке results/cleaner/sessions\n", Colors.red, interval=0.0005)
            return False

        # Создаем клиент
        client = TelegramClient(str(session_file), api_id, api_hash,
                              device_model=device_model,
                              system_version=system_version,
                              app_version=app_version)
        await client.connect()

        if not await client.is_user_authorized():
            Write.Print("\n    [!] Сессия не авторизована\n", Colors.red, interval=0.0005)
            return False

        count = 0
        async for dialog in client.iter_dialogs():
            entity = dialog.entity
            
            should_delete = False
            if dialog_type == 'user' and isinstance(entity, User) and not entity.bot:
                should_delete = True
            elif dialog_type == 'chat' and isinstance(entity, Chat):
                should_delete = True
            elif dialog_type == 'channel' and isinstance(entity, Channel) and not entity.megagroup:
                should_delete = True
            elif dialog_type == 'bot' and isinstance(entity, User) and entity.bot:
                should_delete = True

            if should_delete:
                try:
                    await client.delete_dialog(entity)
                    count += 1
                    Write.Print(f"    [+] Удален диалог: {entity.title if hasattr(entity, 'title') else entity.first_name}\n", 
                              Colors.cyan_to_blue, interval=0.0005)
                except Exception as e:
                    Write.Print(f"    [!] Ошибка при удалении диалога: {str(e)}\n", Colors.red, interval=0.0005)
                    continue

        Write.Print(f"\n    [+] Успешно удалено/выполнен выход из {count} {dialog_type}(ов)\n", 
                   Colors.cyan_to_blue, interval=0.0005)
        logging.info(f"Удалено {count} {dialog_type}(ов)")
        return True

    except Exception as e:
        logging.error(f"Ошибка при очистке диалогов: {e}")
        Write.Print(f"\n    [!] Ошибка: {str(e)}\n", Colors.red, interval=0.0005)
        return False

    finally:
        if 'client' in locals():
            await client.disconnect()
