import asyncio

from tbots.user_bots.user_bot import UserBot

import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class Parser(UserBot):
    def __init__(self, path):
        super().__init__(path, 'Parser')
        self.donners = eval(self._configs[3].split(' = ')[1])
        self.buff_changed_ = False
        self.init_signals()


    def save_configs(self):
        with open(self._path, 'w') as fl:
            to_save = '\n'.join(['[pyrogram]',
                                 'api_id = ' + str(self._api_id),
                                 'api_hash = ' + self._api_hash,
                                 'donner = ' + str(self.donners)])
            fl.write(to_save)

    def add_donner(self, new_donner):
        self.donners.append(new_donner)
        self.save_configs()

    def delete_donner(self, donner_name, delete_all=False):
        if delete_all:
            pass
            self.donners.clear()
        else:
            self.donners.remove(donner_name)
        self.save_configs()

    def init_signals(self):
        @self.client.on_message()
        async def get_post(client, message):
            if not self.power_on:
                return

            username = message.chat.username
            text = message.text
            print(message.text, message.chat)
            self.buff_changed_ = True

            connection = psycopg2.connect(user="postgres",
                                          password="123",
                                          host="127.0.0.1",
                                          port="5432")

            cursor = connection.cursor()
            query = 'INSERT INTO Messages (MESSAGE, LOGIN) values (\'' + str(message.text) + '\' , ' + '\'' + str(message.chat.username) + '\');'
            cursor.execute(query)
            connection.commit()

            query = 'INSERT INTO Users (LOGIN) values (\'' + str(message.chat.username) + '\');'
            cursor.execute(query)
            connection.commit()
            connection.close()

            await self.client.send_message(chat_id=981873870, text=message.text)

#5056351011