import os
import asyncio
import configparser
import json
from pystyle import Write, Colors, Colorate
from utils import count_dialogs, clean_dialogs
from . import print_separator, banner, print_menu_item, print_header

def cleaner_menu(dialog_type):
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print(Colorate.Diagonal(Colors.blue_to_cyan, banner))
        print_separator()
        
        print_header("ОЧИСТКА АККАУНТА")
        print_menu_item("1", "Настроить Device ID", "Изменить Device ID")
        print_menu_item("2", "Настроить API", "Изменить API ID и Hash")
        print_menu_item("3", "Открыть директорию", "Открыть папку с сессиями")
        print_menu_item("4", f"Подсчет {dialog_type}", "Узнать количество каналов")
        print_menu_item("5", "Начать очистку", "Выход из всех каналов")
        print_menu_item("6", "Назад", "Вернуться в главное меню")
        
        print_separator()
        Write.Print("\n    > Выберите пункт меню: ", Colors.cyan_to_blue, interval=0.0005)
        choice = input()

        if choice == "1":
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
                        if 'DLG' not in config:
                            config['DLG'] = {}
                        config['DLG']['device_id'] = str(device_num - 1)
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
        elif choice == "2":
            try:
                Write.Print("\n    Введите API ID > ", Colors.blue_to_cyan, interval=0.0005)
                api_id = input()
                
                Write.Print("    Введите API Hash > ", Colors.blue_to_cyan, interval=0.0005)
                api_hash = input()
                
                config = configparser.ConfigParser()
                config.read('config.ini')
                
                if 'DLG' not in config:
                    config['DLG'] = {}
                    
                config['DLG']['api_id'] = api_id
                config['DLG']['api_hash'] = api_hash
                
                with open('config.ini', 'w') as f:
                    config.write(f)
                    
                Write.Print("\n    [+] API данные успешно сохранены\n", Colors.cyan_to_blue, interval=0.0005)
                
            except Exception as e:
                Write.Print(f"\n    [!] Ошибка: {str(e)}\n", Colors.red, interval=0.0005)
                
            Write.Print("\n    Нажмите Enter для продолжения...", Colors.blue_to_cyan, interval=0.0005)
            input()
        elif choice == "3":
            path = os.path.abspath("results/cleaner/sessions")
            os.makedirs(path, exist_ok=True)
            os.startfile(path) if os.name == 'nt' else os.system(f'xdg-open {path}')
            
        elif choice == "4":
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            count = loop.run_until_complete(count_dialogs(dialog_type))
            if count is False:
                Write.Print("\n    [!] Сессия не авторизована\n", Colors.red, interval=0.0005)
            loop.close()
            Write.Print("\n    Нажмите Enter для продолжения...", Colors.blue_to_cyan, interval=0.0005)
            input()
            
        elif choice == "5":
            Write.Print("\n    [*] Начинаем процесс очистки каналов...\n", Colors.blue_to_cyan, interval=0.0005)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(clean_dialogs(dialog_type))
            if result is False:
                Write.Print("\n    [!] Сессия не авторизована\n", Colors.red, interval=0.0005)
            loop.close()
            if result:
                Write.Print("\n    [+] Очистка завершена успешно\n", Colors.cyan_to_blue, interval=0.0005)
            Write.Print("\n    Нажмите Enter для продолжения...", Colors.blue_to_cyan, interval=0.0005)
            input()
            
        elif choice == "6":
            break
            
        else:
            Write.Print("\n    [!] Неверный выбор. Повторите попытку.\n", Colors.red, interval=0.0005)
            Write.Print("\n    Нажмите Enter для продолжения...", Colors.blue_to_cyan, interval=0.0005)
            input()
