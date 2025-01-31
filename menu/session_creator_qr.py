import os
import json
import configparser
import asyncio
from pystyle import Write, Colors, Colorate
from menu import banner, print_separator
from utils import create_session_qr

def session_creator_qr_menu():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print(Colorate.Diagonal(Colors.blue_to_cyan, banner))
        print_separator()
        Write.Print("\n    ┏━━ Выберите действие:\n", Colors.cyan, interval=0.0005)
        Write.Print("    ┃ 1 ┃ Настроить device\n", Colors.blue_to_cyan, interval=0.0005)
        Write.Print("    ┃ 2 ┃ Настроить API id and hash\n", Colors.blue_to_cyan, interval=0.0005)
        Write.Print("    ┃ 3 ┃ Получить QR код\n", Colors.blue_to_cyan, interval=0.0005)
        Write.Print("    ┃ 4 ┃ Открыть директорию для получения результатов\n", Colors.blue_to_cyan, interval=0.0005)
        Write.Print("    ┃ 5 ┃ Выйти в главное меню\n", Colors.blue_to_cyan, interval=0.0005)
        print_separator()
        Write.Print("\n    > Выберите пункт меню: ", Colors.cyan_to_blue, interval=0.0005)
        subchoice = input()

        if subchoice == "1":
            try:
                with open('src/set_apps.json', 'r', encoding='utf-8') as f:
                    devices = json.load(f)
                
                Write.Print("\n    Доступные устройства:\n", Colors.cyan, interval=0.0005)
                for i, device in enumerate(devices, 1):
                    Write.Print(f"    {i:02d} ┃ {device['device_model']} ({device['system_version']})\n", 
                              Colors.blue_to_cyan, interval=0.0005)
                
                Write.Print("\n    Введите номер устройства > ", Colors.blue_to_cyan, interval=0.0005)
                device_num = input()
                
                try:
                    device_num = int(device_num)
                    if 1 <= device_num <= len(devices):
                        config = configparser.ConfigParser()
                        config.read('config.ini')
                        if 'QR' not in config:
                            config['QR'] = {}
                        config['QR']['device_id'] = str(device_num - 1)
                        with open('config.ini', 'w') as f:
                            config.write(f)
                        Write.Print(f"\n    [+] Устройство {devices[device_num-1]['device_model']} успешно установлено\n", 
                                  Colors.cyan_to_blue, interval=0.0005)
                    else:
                        Write.Print("\n    [!] Неверный номер устройства\n", Colors.red, interval=0.0005)
                except ValueError:
                    Write.Print("\n    [!] Введите корректный номер\n", Colors.red, interval=0.0005)
                    
            except Exception as e:
                Write.Print(f"\n    [!] Ошибка: {str(e)}\n", Colors.red, interval=0.0005)
            Write.Print("\n    Нажмите Enter для продолжения...", Colors.blue_to_cyan, interval=0.0005)
            input()
        elif subchoice == "2":
            try:
                Write.Print("\n    Введите API ID > ", Colors.blue_to_cyan, interval=0.0005)
                api_id = input()
                
                Write.Print("    Введите API Hash > ", Colors.blue_to_cyan, interval=0.0005)
                api_hash = input()
                
                config = configparser.ConfigParser()
                config.read('config.ini')
                
                if 'QR' not in config:
                    config['QR'] = {}
                    
                config['QR']['api_id'] = api_id
                config['QR']['api_hash'] = api_hash
                
                with open('config.ini', 'w') as f:
                    config.write(f)
                    
                Write.Print("\n    [+] API данные успешно сохранены\n", Colors.cyan_to_blue, interval=0.0005)
                
            except Exception as e:
                Write.Print(f"\n    [!] Ошибка: {str(e)}\n", Colors.red, interval=0.0005)
                
            Write.Print("\n    Нажмите Enter для продолжения...", Colors.blue_to_cyan, interval=0.0005)
            input()
        elif subchoice == "3":
            asyncio.run(create_session_qr())
            Write.Print("\n    Нажмите Enter для продолжения...", Colors.blue_to_cyan, interval=0.0005)
            input()
        elif subchoice == "4":
            try:
                folder_path = os.path.abspath('results/create_session_qrcode/sessios')
                os.makedirs(folder_path, exist_ok=True)
                os.startfile(folder_path)
            except Exception as e:
                Write.Print("\n    Ошибка при открытии директории!\n", Colors.blue_to_cyan, interval=0.0005)
        elif subchoice == "5":
            return
        else:
            Write.Print("\n    [!] Неверный выбор\n", Colors.red, interval=0.0005)