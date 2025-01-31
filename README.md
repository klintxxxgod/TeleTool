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

<details>
  <summary><strong>Language</strong></summary>
  <br>
  
![Python](https://img.shields.io/badge/Python-%23000000.svg?style=for-the-badge&logo=python&logoColor=white)

  <br>
</details>

---

## ♥️ Как запустить
Заранее укажете TOKEN вашего бота.
cmd:

   ```bash
  pip install -r requirements.txt  # Установка необходимых библиотек
  python main.py #Запуск бота
  ```
---


## 🖤 Контакты

[![Telegram](https://img.shields.io/badge/-Telegram-black?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/klintxxxgod)  [![Lolz](https://img.shields.io/badge/-Lolz%20Team-black?style=for-the-badge&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAFdJREFUOI3FkjEOgkAQRc/CoFAEmf4SzkIkg1UkfsAdKNFBOkEEVnMkr1SBBSgUtqtUKV9jeBGwrvE3d+7s3TeAH5GgdYBGSCYJ1ASowm5YAz5voFrOh6oP/poM14wHdAe2Bi4OjsMUyccxPB3bs6Dn8AMhRWLZLeQKkwAAAABJRU5ErkJggg==&logoColor=white)](https://lolz.live/klintxxxgod/)  [![BHF](https://img.shields.io/badge/-BHF-black?style=for-the-badge&logo=matrix&logoColor=white)](https://bhf.pro/members/545192/)  [![Gmail](https://img.shields.io/badge/-Gmail-black?style=for-the-badge&logo=gmail&logoColor=white)](mailto:owner.klint@gmail.com)
