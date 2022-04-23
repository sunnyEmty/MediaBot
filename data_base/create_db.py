import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json

with open('database_conf.json', 'r', encoding='utf-8') as f:
    res = json.load(f)

# Подключение к существующей базе данных
connection = psycopg2.connect(**res)
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Курсор для выполнения операций с базой данных
cursor = connection.cursor()
create_table_query = 'CREATE TABLE Users (ID SERIAL, LOGIN TEXT PRIMARY KEY); '
cursor.execute(create_table_query)
create_table_query = 'CREATE TABLE Messages (MESSAGE_ID SERIAL PRIMARY KEY, ' \
                     'MESSAGE TEXT NOT NULL, LOGIN TEXT REFERENCES Users (LOGIN), MEDIA TEXT);'
cursor.execute(create_table_query)
connection.commit()
connection.close()
