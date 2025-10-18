# ru_wordly_24_7

### Угадайте загаданное слово с шести попыток.

- После каждой попытки цвет букв будет меняться, чтобы показать, какие буквы есть в загаданном слове!
- Если буква есть в загаданном слове, но стоит в другом месте, цвет будет желтый.
- Если буква есть в загаданном слове и стоит на правильном месте, её цвет будет зелёным.
- Загадываются существительные в единственном числе.
- В загаданном слове могут быть одинаковые буквы.
- По правилам русских кроссвордов буква Ё в словах заменена на E!

Пиал с нуля, от оригинала отличается тем что не имеет ограничений на количество слов в день.

### Запуск под Linux

- python3 -m venv ./venv
- source ./venv/bin/activate
- pip3 install -r requirements.txt
- python3 main.py

### Собрать apk для Android

Сборку нужно осуществлять на Ubuntu 22.04, на более новых версиях есть проблемы.

Можно собирать в контейнере.

- sudo apt update
- sudo apt install -y git zip unzip openjdk-17-jdk python3-pip python3-venv autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
- python3 -m venv ./venv
- source ./venv/bin/activate
- pip3 install -r requirements.txt
- buildozer init # Создаст файл buildozer.spec, его следует заполнить, пример в buildozer.spec.example
- buildozer -v android debug

Если всё правильно, в каталоге bin появится apk файл.
