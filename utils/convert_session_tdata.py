import os
import logging
import configparser
from pathlib import Path
from telethon.sync import TelegramClient
from opentele.api import UseCurrentSession
from pystyle import Write, Colors

# Настраиваем логирование
logging.basicConfig(
    filename='results/session_to_tdata/converter.log',
    filemode='a', 
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def session_to_tdata_convert():
    # Определяем пути
    sessions_dir = 'results/session_to_tdata/sessions'
    tdatas_dir = 'results/session_to_tdata/tdatas'
    
    # Создаем директории
    os.makedirs(sessions_dir, exist_ok=True)
    os.makedirs(tdatas_dir, exist_ok=True)
    
    # Получаем список .session файлов
    session_files = list(Path(sessions_dir).glob('*.session'))
    
    if not session_files:
        logging.error(f"В директории {sessions_dir} не найдено .session файлов")
        Write.Print("\n    [!] Не найдено .session файлов в директории\n", Colors.red, interval=0.0005)
        return False

    success_count = 0
    total_files = len(session_files)
    
    # Читаем конфиг
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    if 'STD' not in config or not config['STD'].get('api_id') or not config['STD'].get('api_hash'):
        Write.Print("\n    [!] Отсутствуют API параметры в config.ini\n", Colors.red, interval=0.0005)
        return False
        
    api_id = config['STD']['api_id']
    api_hash = config['STD']['api_hash']

    for session_file in session_files:
        try:
            logging.info(f"Конвертация файла: {session_file}")
            Write.Print(f"\n    [*] Конвертация файла: {session_file.name}\n", Colors.blue_to_cyan, interval=0.0005)
            
            # Создаем клиент и конвертируем
            client = TelegramClient(str(session_file), api_id, api_hash)
            await client.connect()
            
            if not await client.is_user_authorized():
                Write.Print(f"    [!] Сессия {session_file.name} не авторизована\n", Colors.red, interval=0.0005)
                continue
                
            tdesk = await client.ToTDesktop(flag=UseCurrentSession)
            tdata_path = os.path.join(tdatas_dir, session_file.stem)
            
            # Сначала удаляем старую директорию если она существует
            if os.path.exists(tdata_path):
                for root, dirs, files in os.walk(tdata_path, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(tdata_path)
                
            # Создаем новую чистую директорию
            os.makedirs(tdata_path)
            
            # Сохраняем tdata
            tdesk.SaveTData(tdata_path)
                
            success_count += 1
            logging.info(f"Успешно конвертирован файл: {session_file.name}")
            Write.Print(f"    [+] Успешно конвертирован файл: {session_file.name}\n", Colors.cyan_to_blue, interval=0.0005)

        except Exception as e:
            logging.error(f"Ошибка при конвертации {session_file}: {e}")
            Write.Print(f"    [!] Ошибка при конвертации {session_file.name}: {e}\n", Colors.red, interval=0.0005)
            continue
            
        finally:
            if 'client' in locals():
                await client.disconnect()

    if success_count > 0:
        logging.info(f"Конвертировано успешно: {success_count} из {total_files} файлов")
        Write.Print(f"\n    [+] Конвертировано успешно: {success_count} из {total_files} файлов\n", Colors.cyan_to_blue, interval=0.0005)
        return True
    else:
        logging.error("Не удалось конвертировать ни одного файла")
        Write.Print("\n    [!] Не удалось конвертировать ни одного файла\n", Colors.red, interval=0.0005)
        return False
