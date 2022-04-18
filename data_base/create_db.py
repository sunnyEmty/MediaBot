import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Подключение к существующей базе данных
connection = psycopg2.connect(user="postgres",
                              password="123",
                              host="127.0.0.1",
                              port="5432")
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Курсор для выполнения операций с базой данных
cursor = connection.cursor()

create_table_query = 'CREATE TABLE Messages (MESSAGE_ID SERIAL PRIMARY KEY, MESSAGE TEXT NOT NULL, LOGIN TEXT NOT NULL); '
cursor.execute(create_table_query)
create_table_query = 'CREATE TABLE Users (ID SERIAL PRIMARY KEY, LOGIN TEXT PRIMARY KEY); '
cursor.execute(create_table_query)
connection.commit()
connection.close()