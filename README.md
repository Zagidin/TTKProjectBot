# Бот ТТК
___
### Запуск **Бота**
___
#### Windows

```shell
 python main.py
```
#### Linux

```shell
 python3 main.py
```

---
### Установка нужных библиотек

---

```shell
pip install -r requirements.txt
```

---

---

## Перед запуском, из папки `text_recognition_library` извлечь архив в корневую папку:
> WIN + R
> 
> sysdm.cpl
#### В появившемся окне перейти по:
> + Дополнительно 
> + переменные среды 
> + PATH 
> + Изменить 
> + Создать `(Ввести ссылку на папку которую извекли из архива)`

---

### Перед запуском, создайте файл `.env`
> API_TOKEN_BOT=<Ваш Токен Бота>

> DATABASE_URL=<Подключение к БД (`ПРИМЕР`: sqlite:///./test.db)>

> FLASK_DATABASE=<Подключение к БД (`ПРИМЕР`: sqlite:///test_flask.db)>

> ADMIN_EMAIL=<Введите почту email>

---
