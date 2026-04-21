import asyncio
import os
import configparser
from opentele.api import CreateNewSession
from opentele.td import TDesktop
from pystyle import Write, Colors

async def tdata_to_session(tdata_path, session_path):
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        if 'TTS' not in config:
            Write.Print("\n    [!] Не найдены настройки в config.ini\n", Colors.red, interval=0.0005)
            return False
            
        tdesk = TDesktop(tdata_path)
        await asyncio.wait_for(
            tdesk.ToTelethon(
                session=session_path,
                flag=CreateNewSession,
                api_id=config['TTS']['api_id'],
                api_hash=config['TTS']['api_hash']
            ),
            timeout=4.0
        )
        return True
    except Exception as e:
        Write.Print(f"\n    [!] Ошибка конвертации: {str(e)}\n", Colors.red, interval=0.0005)
        return False

async def tdata_to_session_convert():
    try:
        base_path = os.getcwd()
        tdatas_dir = os.path.join(base_path, "results/tdata_to_session/tdatas")
        sessions_dir = os.path.join(base_path, "results/tdata_to_session/sessions")
        
        if not os.path.exists(tdatas_dir):
            os.makedirs(tdatas_dir)
            Write.Print("\n    [!] Создана папка для tdata файлов\n", Colors.red, interval=0.0005)
            return False
        
        if not os.path.exists(sessions_dir):
            os.makedirs(sessions_dir)

        tdatas = [f for f in os.listdir(tdatas_dir) if os.path.isdir(os.path.join(tdatas_dir, f))]
        if not tdatas:
            Write.Print("\n    [!] Папка с tdata файлами пуста\n", Colors.red, interval=0.0005)
            return False
        
        success_count = 0
        total_count = len(tdatas)
        
        for tdata in tdatas:
            Write.Print(f"\n    [ ] Конвертация {tdata}...", Colors.blue_to_cyan, interval=0.0005)
            tdata_path = os.path.join(tdatas_dir, tdata)
            session_path = os.path.join(sessions_dir, f"{tdata}.session")
            
            if await tdata_to_session(tdata_path, session_path):
                success_count += 1
                Write.Print(" Успешно!\n", Colors.cyan_to_blue, interval=0.0005)
            else:
                Write.Print(" Ошибка!\n", Colors.red, interval=0.0005)

        Write.Print(f"\n    [+] Конвертировано {success_count} из {total_count} tdata\n", 
                   Colors.cyan_to_blue, interval=0.0005)
        return True if success_count > 0 else False

    except Exception as e:
        Write.Print(f"\n    [!] Критическая ошибка: {str(e)}\n", Colors.red, interval=0.0005)
        return False
