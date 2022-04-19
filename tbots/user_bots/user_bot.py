from pyrogram import Client, idle
import asyncio
from psycopg2 import Error
import psycopg2

class UserBot:
    loop = asyncio.get_event_loop()

    def __init__(self, path, name='UserBot'):
        with open(path) as f:
            self._configs = f.read().splitlines()
            self._api_id = self._configs[1].split(' = ')[1]
            self._api_hash = self._configs[2].split(' = ')[1]
            self.power_on = self._configs[3].split(' = ')[1]
        self.client = Client(name, api_id=self._api_id, api_hash=self._api_hash)
        self._path = path
        self.power_on = True
        self.login()
        self.run_user_bot()
        self.buff = {
            'api_id': None,
            'api_hash': None,
        }

    def _make_configs(self):
        return '\n'.join(['[pyrogram]',
                          'api_id = ' + str(self._api_id),
                          'api_hash = ' + self._api_hash,
                          'power_on = ' + str(self.power_on)])

    async def save_configs(self):
        with open(self._path, 'w') as fl:
            fl.write(self._make_configs())
            await self.client.restart()

    def init_signals(self):
        pass


    def change_account(self, new_id, new_hash):
        self._api_id = new_id
        self._api_hash = new_hash
        self.save_configs()

    @staticmethod
    def db_request(query):
        connection = False
        cursor = False
        err = True
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="123",
                                          host="127.0.0.1",
                                          port="5432")
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            return True
        except (Exception, Error):
            return False
        finally:
            if connection:
                connection.close()
                cursor.close()


    async def _start_user_bot(self):
        await self.client.start()

    def run_user_bot(self):
        UserBot.loop.create_task(self._start_user_bot())


    def login(self):
        self.client.start()
        self.client.stop()

    async def pause_user_bot(self):
        await self.client.stop()






