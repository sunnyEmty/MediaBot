from pyrogram import filters, Client
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
                          'api_id = ' + str(self.api_id),
                          'api_hash = ' + self.api_hash,
                          'power_on = ' + str(self.power_on),
                          'donner = ' + str(self.donners),
                          'get_media = ' + str(self.get_media),
                          'media_path = ' + str(self.media_path),
                          'pic_format = ' + str(self.pic_format)[1:],
                          'regular = ' + self.regular])

    async def save_configs(self):
        with open(self._path, 'w') as fl:
            fl.write(self._make_configs())
        await self.client.stop()
        self.client = Client(self.name, api_id=self.api_id, api_hash=self.api_hash)
        self.run_user_bot()
        self.init_signals()

    def clear_filters(self):
        self.regular = '.*'

    def get_filters(self):
        return set(tuple(self.regular.split('|')))

    def set_reg_from_filters(self, filters_):
        s = set(tuple(filters_))
        self.regular = '|'.join(s)

    def add_filters(self, filters):
        if self.regular == '.*':
            self.regular = '|'.join(set(filters))
            return

        last_filt = self.regular.split('|')
        last_filt += filters
        last_filt = tuple(last_filt)
        self.regular = '|'.join(set(last_filt))

    def erase_filters(self, filts):
        last_filts = set(self.regular.split('|'))
        for filt in filts:
            if filt in last_filts:
                last_filts.remove(filt)

        if last_filts == {}:
            self.regular = '.*'
        else:
            self.regular = '|'.join(last_filts)










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

        @self.client.on_message(filters.chat(self.donners) & filters.regex(self.regular))
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