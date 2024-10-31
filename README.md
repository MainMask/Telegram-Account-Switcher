# Telegram Account Switcher

This guide provides a detailed, step-by-step installation and usage manual for the Telegram Account Switcher script. Follow these instructions carefully to set up and use the script effectively.

---

## English Instructions

### Prerequisites

To run this script, you need to have the following installed:
- Python 3.8 or higher
- Pip (Python package installer)
- Flask library (`pip install Flask`)
- Python-dotenv library (`pip install python-dotenv`)
- Git (for version control)
- Telegram Portable (`Telegram.exe` should be accessible in the system or a defined path)

Ensure that the Telegram Desktop is installed in a portable configuration, allowing easy access to its data folder (tdata).

### Step-by-Step Installation

1. **Clone the Repository**
   - Clone this repository to your local machine:
     ```sh
     git clone <repository-url>
     cd telegram_account_switcher
     ```

2. **Environment Configuration**
   - Create a `.env` file in the root directory and add the following configurations:
     ```sh
     FLASK_APP=main.py
     FLASK_ENV=development
     FLASK_DEBUG=1
     FLASK_RUN_PORT=5000
     TG_PORTABLE_PATH=/path/to/telegram/portable
     TDATA_ACCOUNTS_PATH=/path/to/tdata/accounts
     TG_SYMLINK_PATH=/path/to/telegram/portable/tdata
     PROXY_ACCOUNTS_PATH=/path/to/proxy/accounts
     TELEGRAM_COMMAND=/path/to/telegram/Telegram
     TELEGRAM_WORKDIR=/path/to/telegram/portable
     ```
     Update the paths based on your Telegram Portable installation and tdata accounts directory.

3. **Install Dependencies**
   - Install the required Python libraries:
     ```sh
     pip install -r requirements.txt
     ```
     Ensure the file `requirements.txt` contains the following:
     ```
     Flask
     python-dotenv
     ```

4. **Account Directory Setup**
   - Place the Telegram tdata folders under the configured `TDATA_ACCOUNTS_PATH`.
   - The account folders should be named sequentially as `Account_1`, `Account_2`, etc.

5. **Run the Script**
   - Start the Flask server by executing:
     ```sh
     python main.py
     ```
   - By default, the server runs on `http://127.0.0.1:5000/`.

6. **Using the Web Interface**
   - Access the web interface by visiting `http://127.0.0.1:5000/`.
   - You can select an account from the dropdown menu to switch.
   - Optionally, add proxy details in the provided text field.
   - After pressing "Switch Account", the Telegram instance will restart with the chosen account.

### Troubleshooting
- **Flask Server Fails to Start**: Ensure all environment variables in the `.env` file are correctly set.
- **Symbolic Link Issues**: Check if you have permission to create symbolic links. You may need administrative rights.
- **pkill not working on Windows**: Modify the shutdown command to match Windows (`taskkill /IM Telegram.exe /F`).

## Инструкция на русском языке

### Пререквизиты

Для запуска этого скрипта вам потребуется:
- Python 3.8 или новее
- Pip (установщик пакетов Python)
- Библиотека Flask (`pip install Flask`)
- Библиотека Python-dotenv (`pip install python-dotenv`)
- Git (для управления версиями)
- Telegram Portable (должна быть доступна Telegram.exe)

Убедитесь, что Telegram Desktop установлен в portable-режиме, что облегчает доступ к папке tdata.

### Шаги установки

1. **Клонирование репозитория**
   - Клонируйте этот репозиторий на вашу местную машину:
     ```sh
     git clone <repository-url>
     cd telegram_account_switcher
     ```

2. **Конфигурация окружения**
   - Создайте файл `.env` в корневой папке и добавьте следующие конфигурации:
     ```sh
     FLASK_APP=main.py
     FLASK_ENV=development
     FLASK_DEBUG=1
     FLASK_RUN_PORT=5000
     TG_PORTABLE_PATH=/path/to/telegram/portable
     TDATA_ACCOUNTS_PATH=/path/to/tdata/accounts
     TG_SYMLINK_PATH=/path/to/telegram/portable/tdata
     PROXY_ACCOUNTS_PATH=/path/to/proxy/accounts
     TELEGRAM_COMMAND=/path/to/telegram/Telegram
     TELEGRAM_WORKDIR=/path/to/telegram/portable
     ```
     Обновите пути в соответствии с вашей Telegram Portable и директорией tdata.

3. **Установка зависимостей**
   - Установите нужные библиотеки Python:
     ```sh
     pip install -r requirements.txt
     ```
     Убедитесь, что файл `requirements.txt` содержит следующее:
     ```
     Flask
     python-dotenv
     ```

4. **Настройка директорий аккаунтов**
   - Поместите Telegram tdata папки в конфигурированный `TDATA_ACCOUNTS_PATH`.
   - Папки аккаунтов должны именоваться последовательно: `Account_1`, `Account_2`, и т.д.

5. **Запуск скрипта**
   - Запустите Flask сервер с помощью команды:
     ```sh
     python main.py
     ```
   - По умолчанию сервер запускается на `http://127.0.0.1:5000/`.

6. **Использование веб-интерфейса**
   - Перейдите на `http://127.0.0.1:5000/` для доступа к веб-интерфейсу.
   - Выберите нужный аккаунт из выпадающего списка и переключитесь.
   - При необходимости добавьте прокси в соответствующее поле.
   - После нажатия кнопки "Switch Account" Telegram будет перезапущен с выбранным аккаунтом.

### Устранение ошибок
- **Сервер Flask не запускается**: Проверьте, все ли переменные среды определены в `.env` файле.
- **Проблемы со символической ссылкой**: Проверьте, есть ли у вас права на создание символических ссылок. Могут потребоваться административные права.
- **pkill не работает на Windows**: Модифицируйте команду для закрытия на Windows (толстая стрелка — `taskkill /IM Telegram.exe /F`).

