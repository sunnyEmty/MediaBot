# Для первоначальной настройки бота выполните следующие дествия
1. Введите парамметры создаваемой базы данных в файле
data_base/database_conf.json (это не обязательно)
2. Запусите одиин раз скрипт data_base/create_db.py для создания базы данных (больше его запускать не надо). Для успешной работы скрипта должна быть установлена
PostgreSQL последней версии.

Также для функционированя бота требуется апи айди и хэш телеграмм аккаунта, к которому подключится юзер-бот. Его можно получить по [ссылке](https://my.telegram.org/auth?to=deactivate)

3. Откройте файлик tbots/user_bots/parser_bot/config.ini для задачи начальных парамметров (это делается один раз при установке бота - в процессе работы бота 
их можно будет менять "на лету" в интерфесе).

4. Введите api_id - апи-айди юзер-бота (вместо INPUT_UOUR_API_ID).
например:
api_id = 213123421

5. Введите api_hash - хэш юзер-бота (вместо INPUT_API_HASH)

6. Сохраните результат


Токен чат-бота (который выступает в роли интерфейса - не юзер-бота), лежит в файле 
tbots/control_bot_configs.json.

НАСТОЯТЕЛЬНО РЕКОМЕНДУЕТСЯ создать СВОЕГО чат-бота (со своего аккаунта через BotFather) и помесить его токен в этот файл
в место исходного (так как исходный токен может перестать работать)

7. Запуситите main.py (при последующих запусках запускать нужно только его)

