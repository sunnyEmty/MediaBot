from pyrogram import Client, idle
import asyncio


class UserBot:
    loop = asyncio.get_event_loop()

    def __init__(self, path, name='UserBot'):
        with open(path) as f:
            self._configs = f.read().splitlines()
            self._api_id = self._configs[1].split(' = ')[1]
            self._api_hash = self._configs[2].split(' = ')[1]
        self.client = Client(name, api_id=self._api_id, api_hash=self._api_hash)
        self._path = path
        self.login()
        UserBot.loop.create_task(self.run_user_bot())
        self.buff = {
            'api_id': None,
            'api_hash': None,
            'donner': None
        }

    def save_configs(self):
        with open(self._path, 'w') as fl:
            to_save = '\n'.join(['[pyrogram]',
                                 'api_id = ' + str(self._api_id),
                                 'api_hash = ' + self._api_hash])
            fl.write(to_save)

    def change_account(self, new_id, new_hash):
        self._api_id = new_id
        self._api_hash = new_hash
        self.save_configs()

    async def run_user_bot(self):
        await self.client.start()
        await idle()

    def login(self):
        self.client.start()
        self.client.stop()

    def stop_user_bot(self):
        self.client.stop()




