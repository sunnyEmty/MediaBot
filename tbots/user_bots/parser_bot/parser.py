import re

import pyrogram.types
from pyrogram import filters, Client
from tbots.user_bots.user_bot import UserBot
import os
from tbots.bot_exeoptions import DonnerNameException

class Parser(UserBot):
    def __init__(self, path):
        super().__init__(path, 'Parser')
        self.donners = eval(self.configs[4].split(' = ')[1])
        self.get_media = eval(self.configs[5].split(' = ')[1])
        self.media_path = self.configs[6].split(' = ')[1]
        self.pic_format = self.configs[7].split(' = ')
        self.pic_format = '.' + self.pic_format[1] if len(self.pic_format) > 1 else ''
        self.regular = self.configs[8].split(' = ')[1]
        self.stop_list = eval(self.configs[9].split(' = ')[1])
        self.buff_changed_ = False
        self.buff['donner'] = []
        self.init_signals()
        self.client.connect()

    def make_configs(self):
        conf = super().make_configs()
        new = '\n'.join([
                          'donner = ' + str(self.donners),
                          'get_media = ' + str(self.get_media),
                          'media_path = ' + str(self.media_path),
                          'pic_format = ' + str(self.pic_format)[1:],
                          'regular = ' + self.regular,
                          'stop_list = ' + str(self.stop_list)])
        return '\n'.join([conf, new])

    async def save_configs(self):

        await self.client.stop()
        if not os.path.exists(self.name + '.session'):
            self.client = Client(self.name,
                                 api_id=self.buff['api_id'],
                                 api_hash=self.buff['api_hash'],
                                 phone_number=self.buff['phone'],
                                 password=self.buff['password'])
        else:
            self.client = Client(self.name, api_id=self.api_id, api_hash=self.api_hash)
        with open(self._path, 'w') as fl:
            fl.write(self.make_configs())
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

    def add_stoplist(self, users):
        self.stop_list = list(set(tuple(self.stop_list + users)))
        return

    def erase_stoplist(self, users):
        for user in users:
            if user in self.stop_list:
                self.stop_list.remove(user)

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

    async def get_media_path(self, message):
        if not self.get_media or message.media != 'photo':
            return 'NaN'
        count = len(os.listdir(path=self.media_path))
        file_name = self.media_path + '/' + str(count) + self.pic_format
        try:
            await self.client.download_media(file_name=file_name, message=message, block=False)
        except Exception:
            print('Ошибка загрузки файла:', file_name)
        return file_name

    def join_chats(self):
        for chat in self.donners:
            self.client.join_chat(chat)

    def init_signals(self):

        @self.client.on_message(filters.chat(self.donners) & filters.regex(self.regular, flags=re.IGNORECASE))
        async def get_post(client, message):
            if not self.power_on:
                return

            username = message.from_user.username if message.from_user.username else 'NaN'
            if username in self.stop_list or username == 'NaN':
                return

            self.buff_changed_ = True
            text = message.caption if message.caption else message.text
            text = text.replace('\"', '')
            text = text.replace('\'', '')
            try:
                inp = (str(text), '@' + str(username), await self.get_media_path(message))
            except Exception:
                pass
            put_message = 'INSERT INTO Messages (MESSAGE, LOGIN, MEDIA) values ' + str(inp)

            put_user = 'INSERT INTO Users (LOGIN) values (\'' + '@' + username + '\');'
            find_key = 'SELECT 1 FROM USERS WHERE login = \'' + '@' + str(username) + '\';'
            add_user = True if self.get_request(find_key) is None else False

            if self.put_request(put_user, send_req=add_user) and self.put_request(put_message):
                pass
            else:
                print("Ошбика связи с базой данных")
