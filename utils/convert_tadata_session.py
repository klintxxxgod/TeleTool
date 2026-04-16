<<<<<<< HEAD
import asyncio
import os
import configparser
from typing import List, Optional

from opentele.api import API, APIData, CreateNewSession
from opentele.exception import OpenTeleException
from opentele.td import TDesktop
from opentele.tl import TelegramClient
from pystyle import Write, Colors


def _directory_has_tdata_keys(directory: str) -> bool:
    if not directory or not os.path.isdir(directory):
        return False
    try:
        for name in os.listdir(directory):
            if name.startswith("key_data"):
                return True
    except OSError:
        return False
    return False


async def _safe_disconnect(client) -> None:
    if client is None:
        return
    try:
        if client.is_connected():
            await client.disconnect()
    except Exception:
        pass


def resolve_tdata_base(path: str) -> Optional[str]:
    """
    Находит каталог, где лежат файлы key_data* (настоящий корень tdata).
    Частый случай: в tdatas положили папку portable Telegram, а key_data — внутри tdata/.
    """
    candidates: List[str] = [
        path,
        os.path.join(path, "tdata"),
        os.path.join(path, "Telegram", "tdata"),
    ]
    for candidate in candidates:
        if _directory_has_tdata_keys(candidate):
            return candidate
    return None


async def tdata_to_session(tdata_path, session_path):
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        if 'TTS' not in config:
            Write.Print("\n    [!] Не найдены настройки в config.ini\n", Colors.red, interval=0.0005)
            return False

        resolved = resolve_tdata_base(tdata_path)
        if not resolved:
            Write.Print(
                "\n    [!] Не найден корень tdata (файлы key_data*). "
                "Положите сюда сам каталог tdata или родительскую папку с подкаталогом tdata "
                "(например portable Telegram).\n",
                Colors.red,
                interval=0.0005,
            )
            return False

        if os.path.normpath(resolved) != os.path.normpath(tdata_path):
            Write.Print(
                f"\n    [i] Обнаружен tdata: {resolved}\n",
                Colors.blue_to_cyan,
                interval=0.0005,
            )

        tts = config['TTS']
        passcode_raw = tts.get('tdata_passcode', '').strip()
        passcode = passcode_raw if passcode_raw else None

        read_api = API.TelegramDesktop.Generate(
            system="windows",
            unique_id=os.path.normcase(os.path.normpath(resolved)),
        )
        tdesk = TDesktop(resolved, api=read_api, passcode=passcode)

        out_api = APIData(int(tts['api_id']), tts['api_hash'].strip())
        accounts = list(tdesk.accounts)
        per_account_timeout = max(4.0, 15.0 * len(accounts))

        sessions_dir = os.path.dirname(session_path) or "."
        stem, _ext = os.path.splitext(os.path.basename(session_path))

        if len(accounts) == 1:
            client = None
            try:
                client = await asyncio.wait_for(
                    TelegramClient.FromTDesktop(
                        accounts[0],
                        session=session_path,
                        flag=CreateNewSession,
                        api=out_api,
                    ),
                    timeout=per_account_timeout,
                )
            finally:
                await _safe_disconnect(client)
        else:
            Write.Print(
                f"\n    [i] В tdata несколько аккаунтов ({len(accounts)}), "
                f"будут файлы {stem}_acc*.session\n",
                Colors.blue_to_cyan,
                interval=0.0005,
            )
            for acc in accounts:
                acc_session = os.path.join(
                    sessions_dir, f"{stem}_acc{acc.index}.session"
                )
                client = None
                try:
                    client = await asyncio.wait_for(
                        TelegramClient.FromTDesktop(
                            acc,
                            session=acc_session,
                            flag=CreateNewSession,
                            api=out_api,
                        ),
                        timeout=per_account_timeout,
                    )
                finally:
                    await _safe_disconnect(client)

        return True
    except OpenTeleException as e:
        Write.Print(
            f"\n    [!] Ошибка opentele: {str(e)}\n"
            "    [i] Проверьте: полная папка tdata, локальный пароль ([TTS] tdata_passcode), "
            "официальный Telegram Desktop (форки вроде AyuGram могут не читаться). "
            "Выполните: pip install -r requirements.txt — нужна сборка opentele с GitHub.\n",
            Colors.red,
            interval=0.0005,
        )
        return False
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
=======
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
>>>>>>> 52bae208c01c84fa139228c18362d9264015306d
