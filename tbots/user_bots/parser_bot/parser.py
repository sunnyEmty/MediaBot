from pyrogram import filters
from tbots.user_bots.user_bot import UserBot
import re
import os

class Parser(UserBot):
    def __init__(self, path):
        super().__init__(path, 'Parser')
        self.donners = eval(self._configs[4].split(' = ')[1])
        self.get_media = eval(self._configs[5].split(' = ')[1])
        self.media_path = self._configs[6].split(' = ')[1]
        self.pic_format = self._configs[7].split(' = ')
        self.pic_format = '.' + self.pic_format[1] if len(self.pic_format) > 1 else ''
        self.regular = self._configs[8].split(' = ')[1]

        self.buff_changed_ = False
        self.buff['donner'] = []
        self.init_signals()

    def _make_configs(self):
        return '\n'.join(['[pyrogram]',
                          'api_id = ' + str(self._api_id),
                          'api_hash = ' + self._api_hash,
                          'power_on = ' + str(self.power_on),
                          'donner = ' + str(self.donners),
                          'get_media = ' + str(self.get_media),
                          'media_path = ' + str(self.media_path),
                          'pic_format = ' + str(self.pic_format),
                          'regular = ' + self.regular])


    def set_keywords(self, keywords, complete_match=None):
        pass





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

    def get_media_path(self, message):
        if not self.get_media or message.media != 'photo':
            return 'NaN'
        count = len(os.listdir(path=self.media_path))
        file_name = self.media_path + '/' + str(count) + self.pic_format
        try:
            self.client.download_media(file_name=file_name, message=message, block=False)
        except Exception:
            print('Ошибка загрузки файла:', file_name)
        return file_name

    def init_signals(self):

        @self.client.on_message(filters.chat(self.donners))
        def get_post(client, message):
            print(message.text)
            if not self.power_on:
                return

            self.buff_changed_ = True
            text = message.caption if message.caption else message.text
            inp = (str(text), '@' + str(message.chat.username), self.get_media_path(message))
            put_message = 'INSERT INTO Messages (MESSAGE, LOGIN, MEDIA) values ' + str(inp)


            put_user = 'INSERT INTO Users (LOGIN) values (\'' + '@' + str(message.chat.username) + '\');'
            if self.db_request(put_user) and self.db_request(put_message):
                pass
            else:
                print("Ошбика связи с базой данных")

            #await self.client.send_message(chat_id=981873870, text=message.text)

#5056351011