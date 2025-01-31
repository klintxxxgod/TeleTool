import os
import json
import sqlite3
from pathlib import Path
import logging

# Настраиваем логирование в файл
logging.basicConfig(
    filename='results/session_analyzer/session_parser.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def session_analyzer_info():
    # Определяем пути к директориям
    sessions_dir = 'results/session_analyzer/sessions'
    dumps_dir = 'results/session_analyzer/dumps'
    
    # Создаем директории если они не существуют
    os.makedirs(sessions_dir, exist_ok=True)
    os.makedirs(dumps_dir, exist_ok=True)
    
    # Получаем список всех .session файлов
    session_files = list(Path(sessions_dir).glob('*.session'))
    
    if not session_files:
        logging.error(f"В директории {sessions_dir} не найдено .session файлов")
        return False
    
    success_count = 0
    total_files = len(session_files)
    
    for session_file in session_files:
        conn = None
        try:
            logging.info(f"Обработка файла: {session_file}")
            conn = sqlite3.connect(session_file)
            cursor = conn.cursor()
            
            # Получаем данные сессии
            cursor.execute("SELECT dc_id, server_address, port, auth_key, takeout_id FROM sessions;")
            sessions = cursor.fetchone()
            session_data = {}
            if sessions:
                session_data = {
                    "dc_id": sessions[0],
                    "server_address": sessions[1],
                    "port": sessions[2],
                    "auth_key": str(sessions[3].hex()) if sessions[3] else None,
                    "takeout_id": sessions[4]
                }

            # Получаем версию
            cursor.execute("SELECT version FROM version;")
            version_row = cursor.fetchone()
            if version_row:
                session_data["version"] = version_row[0]

            # Создаем JSON файл в папке dumps
            json_filename = os.path.join(dumps_dir, f"{session_file.stem}_info.json")
            
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=4, ensure_ascii=False)
                
            success_count += 1
            logging.info(f"Успешно обработан файл: {session_file.name}")

        except Exception as e:
            logging.error(f"Ошибка при обработке файла {session_file}: {e}")
            continue
            
        finally:
            if conn:
                conn.close()
    
    if success_count > 0:
        logging.info(f"Обработано успешно: {success_count} из {total_files} файлов")
        return True
    else:
        logging.error("Не удалось обработать ни одного файла")
        return False