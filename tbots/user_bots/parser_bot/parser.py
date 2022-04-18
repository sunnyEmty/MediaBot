from pyrogram import filters
from tbots.user_bots.user_bot import UserBot
import os

class Parser(UserBot):
    def __init__(self, path):
        super().__init__(path, 'Parser')
        self.donners = eval(self._configs[3].split(' = ')[1])
        self.get_media = eval(self._configs[4].split(' = ')[1])
        self.buff_changed_ = False
        self.buff['donner'] = []
        self.init_signals()

    def _make_configs(self):
        return '\n'.join(['[pyrogram]',
                          'api_id = ' + str(self._api_id),
                          'api_hash = ' + self._api_hash,
                          'donner = ' + str(self.donners)])






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

    def get_media_path(self, media):
        if not self.get_media or media is None:
            return 'NaN'
        count = os.listdir(path= 'media')








    def init_signals(self):

        @self.client.on_message(filters.chat(self.donners))
        def get_post(client, message):
            if not self.power_on:
                return

            print(message.text, message.chat)
            self.buff_changed_ = True

            inp = (str(message.text), str(message.chat.username)) + self.get_media_path(message.media)

            put_message = 'INSERT INTO Messages (MESSAGE, LOGIN, MEDIA) values ' + str(inp)
            print(put_message)
            put_user = 'INSERT INTO Users (LOGIN) values (\'' + str(message.chat.username) + '\');'
            if self.db_request(put_user) and self.db_request(put_message):
                pass
            else:
                print("Ошбика связи с базой данных")

            #await self.client.send_message(chat_id=981873870, text=message.text)

#5056351011