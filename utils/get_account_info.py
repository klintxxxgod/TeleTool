import os
import json
import sqlite3
import configparser
from pathlib import Path
import logging
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.account import GetAuthorizationsRequest as GetSessionsRequest
import asyncio
from pystyle import Write, Colors

# Настраиваем логирование в файл
logging.basicConfig(
    filename='results/account_info_save/session_parser.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def account_info_save_info():
    # Определяем пути к директориям
    sessions_dir = 'results/account_info_save/sessions'
    dumps_dir = 'results/account_info_save/dumps'
    
    # Создаем директории если они не существуют
    os.makedirs(sessions_dir, exist_ok=True)
    os.makedirs(dumps_dir, exist_ok=True)
    
    # Получаем список всех .session файлов
    session_files = list(Path(sessions_dir).glob('*.session'))
    
    if not session_files:
        logging.error(f"В директории {sessions_dir} не найдено .session файлов")
        Write.Print("\n    [!] Не найдено .session файлов в директории\n", Colors.red, interval=0.0005)
        return False
    
    success_count = 0
    total_files = len(session_files)

    # API данные для подключения
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    if 'CHECK' not in config or not config['CHECK'].get('api_id') or not config['CHECK'].get('api_hash') or not config['CHECK'].get('device_id'):
        Write.Print("\n    [!] Отсутствуют необходимые параметры в config.ini\n", Colors.red, interval=0.0005)
        Write.Print("    [!] Пожалуйста, настройте API ID/hash и device в меню\n", Colors.red, interval=0.0005)
        return False
        
    api_id = config['CHECK']['api_id']
    api_hash = config['CHECK']['api_hash']
    device_id = int(config['CHECK']['device_id'])

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
    
    for session_file in session_files:
        try:
            logging.info(f"Обработка файла: {session_file}")
            Write.Print(f"\n    [*] Обработка файла: {session_file.name}\n", Colors.blue_to_cyan, interval=0.0005)
            
            # Создаем клиент и подключаемся
            client = TelegramClient(str(session_file), api_id, api_hash,
                                  device_model=device_model,
                                  system_version=system_version,
                                  app_version=app_version)
            await client.connect()
            
            if not await client.is_user_authorized():
                logging.error(f"Сессия {session_file.name} не авторизована")
                Write.Print(f"    [!] Сессия {session_file.name} не авторизована\n", Colors.red, interval=0.0005)
                continue

            account_info = {}
            
            # Получаем информацию о пользователе
            me = await client.get_me()
            account_info["user_info"] = {
                "user_id": me.id,
                "first_name": me.first_name,
                "last_name": me.last_name,
                "username": me.username,
                "phone": me.phone,
                "premium": me.premium,
                "verified": me.verified,
                "restricted": me.restricted,
                "scam": me.scam,
                "fake": me.fake,
                "bot": me.bot,
                "lang_code": me.lang_code,
                "access_hash": me.access_hash
            }

            # Получаем все диалоги с детальной информацией
            dialogs = await client.get_dialogs()
            account_info["dialogs"] = []
            
            for dialog in dialogs:
                dialog_info = {
                    "id": dialog.id,
                    "name": dialog.name,
                    "title": dialog.title,
                    "is_user": dialog.is_user,
                    "is_group": dialog.is_group,
                    "is_channel": dialog.is_channel,
                    "unread_count": dialog.unread_count,
                    "unread_mentions_count": dialog.unread_mentions_count,
                    "entity_type": str(type(dialog.entity).__name__)
                }
                
                if dialog.entity:
                    entity_info = {
                        "id": dialog.entity.id
                    }
                    
                    # Проверяем наличие атрибутов перед добавлением
                    if hasattr(dialog.entity, "access_hash"):
                        entity_info["access_hash"] = dialog.entity.access_hash
                    if hasattr(dialog.entity, "username"):
                        entity_info["username"] = dialog.entity.username
                    if hasattr(dialog.entity, "participants_count"):
                        entity_info["participants_count"] = dialog.entity.participants_count
                        
                    dialog_info["entity"] = entity_info
                        
                account_info["dialogs"].append(dialog_info)

            # Получаем информацию о всех активных сессиях
            sessions = await client(GetSessionsRequest())
            account_info["sessions"] = []
            
            for auth in sessions.authorizations:
                session_info = {
                    "hash": auth.hash,
                    "device_model": auth.device_model,
                    "platform": auth.platform,
                    "system_version": auth.system_version,
                    "api_id": auth.api_id,
                    "app_name": auth.app_name,
                    "app_version": auth.app_version,
                    "date_created": auth.date_created.isoformat(),
                    "date_active": auth.date_active.isoformat(),
                    "ip": auth.ip,
                    "country": auth.country,
                    "region": auth.region
                }
                account_info["sessions"].append(session_info)

            # Получаем детальную информацию о контактах
            from telethon.tl.functions.contacts import GetContactsRequest
            contacts = await client(GetContactsRequest(hash=0))
            account_info["contacts"] = []
            
            for user in contacts.users:
                contact_info = {
                    "id": user.id,
                    "access_hash": user.access_hash,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "phone": user.phone,
                    "bot": user.bot,
                    "mutual_contact": user.mutual_contact,
                    "verified": user.verified,
                    "restricted": user.restricted,
                    "scam": user.scam,
                    "fake": user.fake,
                    "lang_code": user.lang_code if hasattr(user, "lang_code") else None
                }
                account_info["contacts"].append(contact_info)

            # Сохраняем всю информацию в JSON
            json_filename = os.path.join(dumps_dir, f"{session_file.stem}_full_info.json")
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(account_info, f, indent=4, ensure_ascii=False)
                
            success_count += 1
            logging.info(f"Успешно обработан файл: {session_file.name}")
            Write.Print(f"    [+] Успешно обработан файл: {session_file.name}\n", Colors.cyan_to_blue, interval=0.0005)

        except Exception as e:
            logging.error(f"Ошибка при обработке файла {session_file}: {e}")
            Write.Print(f"    [!] Ошибка при обработке файла {session_file.name}: {e}\n", Colors.red, interval=0.0005)
            continue
            
        finally:
            if 'client' in locals():
                await client.disconnect()
    
    if success_count > 0:
        logging.info(f"Обработано успешно: {success_count} из {total_files} файлов")
        Write.Print(f"\n    [+] Обработано успешно: {success_count} из {total_files} файлов\n", Colors.cyan_to_blue, interval=0.0005)
        return True
    else:
        logging.error("Не удалось обработать ни одного файла")
        Write.Print("\n    [!] Не удалось обработать ни одного файла\n", Colors.red, interval=0.0005)
        return False