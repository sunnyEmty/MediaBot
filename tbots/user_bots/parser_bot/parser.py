from pyrogram import Client, filters
from tbots.user_bots.user_bot import UserBot
import threading
import sqlite3 as sql
'''
with open('config.ini') as f:
    data = f.read().splitlines()
    api_id = data[1].split(' = ')[1]
    api_hash = data[2].split(' = ')[1]
    donner = eval(data[3].split(' = ')[1])

parer_bot = Client('ParserBot', api_id=api_id, api_hash=api_hash)


def save_configs():
    with open('config.ini', 'w') as fl:
        to_save = '\n'.join(['[pyrogram]',
                             'api_id = ' + str(api_id),
                             'api_hash = ' + api_hash,
                             'donner = ' + str(donner) + '\n'])
        fl.write(to_save)


def change_account(new_id, new_hash):
    global api_id, api_hash
    api_id = new_id
    api_hash = new_hash
    save_configs()


def add_donner(new_donner):
    donner.append(new_donner)
    save_configs()


def delete_donner(donner_id, delete_all=False):
    global donner
    if delete_all:
        donner = []
    else:
        donner.remove(donner_id)
    save_configs()


def handle_control
def run_parsing():
    pass
'''

class Parser(UserBot):
    def __init__(self, path):
        super().__init__(path)
        self._donner = eval(self._configs[3].split(' = ')[1])

    def save_configs(self):
        with open(self._path, 'w') as fl:
            to_save = '\n'.join(['[pyrogram]',
                                 'api_id = ' + str(self._api_id),
                                 'api_hash = ' + self._api_hash,
                                 'donner = ' + str(self._donner) + '\n'])
            fl.write(to_save)

    def add_donner(self, new_donner):
        self._donner.append(new_donner)
        self.save_configs()

    def delete_donner(self, donner_name, delete_all=False):
        if delete_all:
            self._donner.clear()
        else:
            self._donner.remove(donner_name)
        self.save_configs()






Parser('C:/Users/User/PycharmProjects/MediaBot/tbots/user_bots/parser_bot/config.ini').delete_donner('dobbb')
