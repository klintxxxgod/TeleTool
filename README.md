# 🖤 Tele Tool!

![Header](https://i.ibb.co/W408CSt1/image.png)


---

## ♥️ О проекте

**Tele Tool** — Инструмент для работы с Telegram сессиями. Программа предоставляет полный набор функций для управления и конвертации Telegram аккаунтов, делая процесс максимально простым и эффективным.

---



## 🖤 Основные возможности:
<details>
  <summary><strong>📂 КАТЕГОРИЯ: 💫 Операции с сессиями</strong></summary>
  <br>
  
  <details>
    <summary><strong>└─ 💨 Анализ сессии</strong></summary>
    <br>
    
    1. Настройка device (Предлагает на выбор конфигурации девайсов для входа в сессию от их лица)
    2. Настройка API id and hash (Настройка данных для подключения к Telegram API)
    3. Открытие директории для загрузки данных (Папка для .session файлов)
    4. Открытие директории для получения результатов (Папка с результатами анализа)
    5. Анализ аккаунта (Получение полной информации о сессии в JSON формате)
    
    
  </details>

  <details>
    <summary><strong>└─ 💨 Создать session через QR</strong></summary>
    <br>
    1. Настройка device (Выбор устройства для авторизации)
    2. Настройка API id and hash
    3. Получение QR кода (Генерация QR-кода для сканирования в приложении Telegram)
    4. Открытие директории с результатами (Доступ к созданным .session файлам)
    5. Поддержка двухфакторной аутентификации
    <br>
  </details>

  <details>
    <summary><strong>└─ 💨 Создать session через код</strong></summary>
    <br>
    1. Настройка device (Выбор устройства для авторизации)
    2. Настройка API id and hash
    3. Получение кода (Ввод номера телефона и кода подтверждения)
    4. Открытие директории с результатами
    5. Поддержка двухфакторной аутентификации
    <br>
  </details>
</details>

<details>
  <summary><strong>📂 КАТЕГОРИЯ: 🔄 Конвертация</strong></summary>
  <br>
  
  <details>
    <summary><strong>└─ 💨 Session ➜ Tdata</strong></summary>
    <br>
    1. Конвертация .session файлов в формат Telegram Desktop (tdata)
    2. Открытие директории для загрузки .session файлов
    3. Открытие директории с результатами конвертации
    4. Сохранение всех настроек и авторизационных данных
    <br>
  </details>

  <details>
    <summary><strong>└─ 💨 Tdata ➜ Session</strong></summary>
    <br>
    1. Конвертация tdata в формат .session
    2. Открытие директории для загрузки tdata
    3. Открытие директории с результатами конвертации
    4. Сохранение всех настроек и авторизационных данных
    <br>
  </details>

  <details>
    <summary><strong>└─ 💨 Session ➜ Info</strong></summary>
    <br>
    1. Извлечение информации из .session файлов
    2. Сохранение в JSON формате:
       - Информация о пользователе
       - Список диалогов
       - Активные сессии
       - Контакты
       - Статистика сообщений
    3. Открытие директории для загрузки .session файлов
    4. Открытие директории с результатами анализа
    <br>
  </details>
</details>

<details>
  <summary><strong>📂 КАТЕГОРИЯ: 🧹 Управление и очистка</strong></summary>
  <br>
  
  <details>
    <summary><strong>└─ 💨 Очистка каналов</strong></summary>
    <br>
    1. Настройка device и API
    2. Массовый выход из каналов
    3. Подсчет количества каналов до и после очистки
    4. Возможность выборочной очистки
    5. Логирование процесса очистки
    <br>
  </details>

  <details>
    <summary><strong>└─ 💨 Очистка групп</strong></summary>
    <br>
    1. Настройка device и API
    2. Массовый выход из групп
    3. Подсчет количества групп до и после очистки
    4. Возможность выборочной очистки
    5. Логирование процесса очистки
    <br>
  </details>

  <details>
    <summary><strong>└─ 💨 Очистка ботов</strong></summary>
    <br>
    1. Настройка device и API
    2. Массовая блокировка ботов
    3. Подсчет количества ботов до и после очистки
    4. Возможность выборочной очистки
    5. Логирование процесса очистки
    <br>
  </details>

  <details>
    <summary><strong>└─ 💨 Очистка диалогов</strong></summary>
    <br>
    1. Настройка device и API
    2. Массовое удаление личных чатов
    3. Подсчет количества диалогов до и после очистки
    4. Возможность выборочной очистки
    5. Логирование процесса очистки
    <br>
  </details>
</details>

---

## ⚙️ Используемые технологии

### 🛠️ Основные библиотеки</strong></summary>
![Python](https://img.shields.io/badge/Python-%23000000.svg?style=for-the-badge&logo=python&logoColor=white) ![Telethon](https://img.shields.io/badge/Telethon-%23000000.svg?style=for-the-badge&logo=telegram&logoColor=white) ![OpenTele](https://img.shields.io/badge/OpenTele-%23000000.svg?style=for-the-badge&logo=telegram&logoColor=white)![PyStyle](https://img.shields.io/badge/PyStyle-%23000000.svg?style=for-the-badge&logo=python&logoColor=white) ![Colorama](https://img.shields.io/badge/Colorama-%23000000.svg?style=for-the-badge&logo=python&logoColor=white) ![ConfigParser](https://img.shields.io/badge/ConfigParser-%23000000.svg?style=for-the-badge&logo=python&logoColor=white) ![AsyncIO](https://img.shields.io/badge/AsyncIO-%23000000.svg?style=for-the-badge&logo=python&logoColor=white)

---

## 📋 Требования

### 💻 Системные требования:
- Python 3.8 или выше (желательно 3.11.6)
- Windows операционная система
- Минимум 100MB свободного места
- Стабильное подключение к интернету
- RAM: минимум 2GB

### 🔑 Telegram API:
- API ID (получить на my.telegram.org)
- API Hash (получить на my.telegram.org)
- Активный Telegram аккаунт
- Доступ к Telegram API

---

## 🌳 Структура проекта

```bash
Telegram-Toolkit/
├── 📁 menu/               # Модули меню
│   ├── banner.py         # Отрисовка баннера и разделителей
│   ├── session_analyzer.py       # Меню анализа сессий
│   ├── session_creator_qr.py      # Создание сессий через QR
│   ├── session_creator_code.py   # Авторизация по коду
│   └── cleaner_and_info.py       # Управление очисткой аккаунта
│
├── 📁 utils/             # Вспомогательные модули
│   ├── get_account_info.py      # Парсинг информации об аккаунте
│   ├── create_session_qrcode.py # Генерация QR-кодов
│   ├── convert_session_tdata.py # Конвертация session → tdata 
│   ├── convert_tadata_session.py # Конвертация tdata → session
│   └── clener_dialogs.py        # Логика очистки диалогов
│
├── 📁 src/               # Ресурсы проекта
│   └── set_apps.json     # База устройств для эмуляции
│
├── 📁 results/            # Результаты работы
│   ├── account_info_save/ # Дампы информации аккаунтов
│   ├── session_analyzer/  # Результаты анализа сессий
│   └── create_session_*/  # Созданные session-файлы
│
├── 📄 main.py            # Главный исполняемый файл
├── 📄 config.ini         # Конфигурация API и устройств
├── 📄 requirements.txt   # Зависимости проекта
└── 📄 run.bat            # Скрипт запуска для Windows
```

### Пояснения к структуре:
1. **Ядро системы** (`main.py`) - Центральный модуль, управляющий всей логикой приложения
2. **Меню-модули** - Группа файлов реализующих интерактивный интерфейс
3. **Утилиты** - Набор "движков" для выполнения основных операций
4. **Конфигурация** - Файлы настроек и пресетов устройств
5. **Результаты** - Автоматически генерируемые в процессе работы данные

---

## 🚀 Руководство по запуску

### 1. Клонирование репозитория
```bash
git clone https://github.com/klintxxxgod/TeleTool
cd TeleTool
```

### 2. Настройка окружения
```bash
# Создание виртуального окружения (Windows)
python -m venv venv
venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt
```

### 3. Настройка конфигурации
1. Получите API ID и Hash на [my.telegram.org](https://my.telegram.org/apps)
2. Отредактируйте `config.ini`:
```ini
[QR]
device_id = 0
api_id = YOUR_API_ID       # Замените на свои значения
api_hash = YOUR_API_HASH   # 32-символьная строка
```

### 4. Запуск приложения
```bash
# Стандартный запуск
python main.py

# Или через bat-файл (Windows)
run.bat
```

### 🛠 Первый запуск:
1. При открытии любого меню где требуется Telegram API приступайте к пункту 2 и 3
2. Настройте device (рекомендуется выбор 0 - Xiaomi)
3. Введите валидные API данные
4. Следуйте инструкциям на экране

![Пример работы](https://i.ibb.co/W408CSt1/image.png)

### ⚠️ Важно!
- Используйте только свои API ключи
- Не делитесь файлами `.session` и `tdata`
- При ошибках проверьте логи в `results/*/*.log`


## 🖤 Контакты

[![Telegram](https://img.shields.io/badge/-Telegram-black?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/klintxxxgod)  [![Lolz](https://img.shields.io/badge/-Lolz%20Team-black?style=for-the-badge&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAFdJREFUOI3FkjEOgkAQRc/CoFAEmf4SzkIkg1UkfsAdKNFBOkEEVnMkr1SBBSgUtqtUKV9jeBGwrvE3d+7s3TeAH5GgdYBGSCYJ1ASowm5YAz5voFrOh6oP/poM14wHdAe2Bi4OjsMUyccxPB3bs6Dn8AMhRWLZLeQKkwAAAABJRU5ErkJggg==&logoColor=white)](https://lolz.live/klintxxxgod/)  [![BHF](https://img.shields.io/badge/-BHF-black?style=for-the-badge&logo=matrix&logoColor=white)](https://bhf.pro/members/545192/)  [![Gmail](https://img.shields.io/badge/-Gmail-black?style=for-the-badge&logo=gmail&logoColor=white)](mailto:owner.klint@gmail.com)
