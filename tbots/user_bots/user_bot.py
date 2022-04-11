from pyrogram import Client
import asyncio


class UserBot:
    def __init__(self, path, name='UserBot'):
        with open(path) as f:
            self._configs = f.read().splitlines()
            self._api_id = self._configs[1].split(' = ')[1]
            self._api_hash = self._configs[2].split(' = ')[1]
        self.user_bot = Client(name, api_id=self._api_id, api_hash=self._api_hash)
        self._path = path

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

    async def configure_t(self, ):

        pass

    async def handler_t(self):

        pass


