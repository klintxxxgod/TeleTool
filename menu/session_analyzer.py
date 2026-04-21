import os
import asyncio
import json
from colorama import *
from utils import session_analyzer_info
from pystyle import Write, Colors, Colorate
from menu import banner, print_separator
    
def session_analyzer_menu():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print(Colorate.Diagonal(Colors.blue_to_cyan, banner))
        print_separator()
        Write.Print("\n    ┏━━ Выберите действие:\n", Colors.cyan, interval=0.0005)
        Write.Print("    ┃ 1 ┃ Открыть директорию для загрузки данных\n", Colors.blue_to_cyan, interval=0.0005)
        Write.Print("    ┃ 2 ┃ Открыть директорию для получения результатов\n", Colors.blue_to_cyan, interval=0.0005)
        Write.Print("    ┃ 3 ┃ Начать анализ\n", Colors.blue_to_cyan, interval=0.0005)
        Write.Print("    ┃ 4 ┃ Выйти в главное меню\n", Colors.blue_to_cyan, interval=0.0005)
        print_separator()
        Write.Print("\n    > Выберите пункт меню: ", Colors.cyan_to_blue, interval=0.0005)
        subchoice = input()

        if subchoice == "1":
            try:
                folder_path = os.path.abspath('results/session_analyzer/sessions')
                os.makedirs(folder_path, exist_ok=True)
                os.startfile(folder_path)
            except Exception as e:
                Write.Print("\n    Ошибка при открытии директории!\n", Colors.blue_to_cyan, interval=0.0005)
        elif subchoice == "2":
            try:
                folder_path = os.path.abspath('results/session_analyzer/dumps')
                os.makedirs(folder_path, exist_ok=True)
                os.startfile(folder_path)
            except Exception as e:
                Write.Print("\n    Ошибка при открытии директории!\n", Colors.blue_to_cyan, interval=0.0005)
        elif subchoice == "3":
            Write.Print("\n    [ ] Начинаем анализ файлов...\n", Colors.blue_to_cyan, interval=0.0005)
            result = asyncio.run(session_analyzer_info())
            if result:
                Write.Print(f"\n    [+] Анализ успешно завершен\n    [+] Результаты сохранены в папке results/session_analyzer/dumps\n", Colors.cyan_to_blue, interval=0.0005)
            else:
                Write.Print("\n    [!] Ошибка анализа! Проверьте наличие .session файлов в папке sessions\n", Colors.red, interval=0.0005)
            Write.Print("\n    Нажмите Enter для продолжения...", Colors.blue_to_cyan, interval=0.0005)
            input()
        elif subchoice == "4":
            return
        else:
            Write.Print("\n    [!] Неверный выбор\n", Colors.red, interval=0.0005)
            Write.Print("\n    Нажмите Enter для продолжения...", Colors.blue_to_cyan, interval=0.0005)
            input()