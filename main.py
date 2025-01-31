import os
from pystyle import *
from colorama import *
from menu import session_analyzer_menu, session_creator_qr_menu, print_separator, banner, print_menu_item, print_header, session_creator_code_menu, session_account_info_menu, session_to_tdata_menu, tdata_to_session_menu, cleaner_menu

# Очистка консоли
os.system('clear' if os.name == 'posix' else 'cls')


def main_menu():
    # Очистка экрана и вывод баннера
    os.system('clear' if os.name == 'posix' else 'cls')
    print(Colorate.Diagonal(Colors.blue_to_cyan, banner))
    print_separator()
    
    # Основное меню
    print_header("ОПЕРАЦИИ С СЕССИЯМИ")
    print_menu_item("01", "Анализ сессии", "Анализ аккаунта Telegram по .session")
    print_menu_item("02", "Создать session через QR", "Сканирование QR-кода")
    print_menu_item("03", "Создать session через код", "Авторизация по коду")
    
    print_header("КОНВЕРТАЦИЯ")
    print_menu_item("04", "Session --> Tdata", "Конвертация в формат Desktop")
    print_menu_item("05", "Tdata --> Session", "Конвертация в формат Telethon")
    print_menu_item("06", "Session --> Info", "Извлечение данных из .session в JSON")
    
    print_header("УПРАВЛЕНИЕ")
    print_menu_item("07", "Очистка каналов", "Массовый выход из каналов")
    print_menu_item("08", "Очистка групп", "Массовый выход из групп") 
    print_menu_item("09", "Удаление ботов", "Блокировка всех ботов")
    print_menu_item("10", "Очистка диалогов", "Удаление личных чатов")
    
    print_header("СИСТЕМА")
    print_menu_item("11", "Контакты разработчика", "Информация о разработчике")
    print_menu_item("12", "Документация", "Информация о разработчике")
    print_menu_item("13", "Выход", "Завершение работы")
    
    print_separator()
    Write.Print("\n    > Выберите пункт меню: ", Colors.cyan_to_blue, interval=0.0005)
    return input()

while True:
    choice = main_menu()

    if choice == "01" or choice == "1":
        session_account_info_menu()
    elif choice == "02" or choice == "2":
        session_creator_qr_menu()
    elif choice == "03" or choice == "3":
        session_creator_code_menu()
    elif choice == "04" or choice == "4":
        session_to_tdata_menu()
    elif choice == "05" or choice == "5":
        tdata_to_session_menu()
    elif choice == "06" or choice == "6":
        session_analyzer_menu()
    elif choice == "07" or choice == "7":
        cleaner_menu("channel")
    elif choice == "08" or choice == "8":
        cleaner_menu("chat")
    elif choice == "09" or choice == "9":
        cleaner_menu("bot")
    elif choice == "10":
        cleaner_menu("user")    
    elif choice == "11":        
        Write.Print("\n    [+] Контакты разработчика:\n", Colors.cyan_to_blue, interval=0.0005)
        Write.Print("\n    • Telegram: ", Colors.cyan_to_blue, interval=0.0005)
        Write.Print("@klintxxxgod", Colors.blue_to_cyan, interval=0.0005)
        Write.Print("\n    • LOLZ: ", Colors.cyan_to_blue, interval=0.0005) 
        Write.Print("KLINTXXXGOD", Colors.blue_to_cyan, interval=0.0005)
        Write.Print("\n    • BHF: ", Colors.cyan_to_blue, interval=0.0005)
        Write.Print("KLINTXXXGOD", Colors.blue_to_cyan, interval=0.0005)
        Write.Print("\n    • GitHub: ", Colors.cyan_to_blue, interval=0.0005)
        Write.Print("klintxxxgod", Colors.blue_to_cyan, interval=0.0005)
        Write.Print("\n\n    Нажмите Enter для продолжения...", Colors.blue_to_cyan, interval=0.0005)
        input()
    elif choice == "12":
        import webbrowser
        Write.Print("\n    [+] Открываю документацию в браузере...\n", Colors.cyan_to_blue, interval=0.0005)
        webbrowser.open('https://github.com/klintxxxgod/TeleTool')
        Write.Print("\n    Нажмите Enter для продолжения...", Colors.blue_to_cyan, interval=0.0005)
        input()
    elif choice == "13":
        Write.Print("\n    [+] Завершение работы...\n", Colors.cyan_to_blue, interval=0.0005)
        break
    else:
        Write.Print("\n    [!] Неверный выбор. Повторите попытку.\n", Colors.red, interval=0.0005)
        Write.Print("\n    Нажмите Enter для продолжения...", Colors.blue_to_cyan, interval=0.0005)
        input()
