Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/MacOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

# Укорачиватель ссылок
Укорачивает Вашу введенную ссылку.
Работает в пользовательском интерфейсе
И по API

# Технологии:
flask==2.0.2, Python3.9.7

# Установка проекта
## Клонируйте репозиторий на локальный компьютер:
```git@github.com:Ninefiveblade/yacut.git```
## Перейдите в папку проекта:
```cd yacut```

# Подготовка к запуску проекта:
Необходимо установить виртуальное окружение:
```python3.9 -m pip install --upgrade pip```
Установить зависимости:
```source venv/bin/activate```
```(venv) $ pip install -r requirements```

# Запуск проекта:
Выполните 
``` (venv) flask run ```

# Протестировать ссылки
``` http://127.0.0.1:5000/ ```
``` http://127.0.0.1:5000/id/{код_короткой_ссылки} ```
``` http://127.0.0.1:5000/api/id/ ```
``` http://127.0.0.1:5000/api/id/{код_короткой_ссылки} ```

# Лицензия:
[LICENSE MIT](LICENSE)

# Aвтор:
[Алексеев Иван](https://github.com/Ninefiveblade)
