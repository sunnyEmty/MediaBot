from tbots.user_bots.user_bot import UserBot


class Parser(UserBot):
    def __init__(self, path):
        super().__init__(path, 'Parser')
        self._donners = eval(self._configs[3].split(' = ')[1])
        self.init_signals()

    def save_configs(self):
        with open(self._path, 'w') as fl:
            to_save = '\n'.join(['[pyrogram]',
                                 'api_id = ' + str(self._api_id),
                                 'api_hash = ' + self._api_hash,
                                 'donner = ' + str(self._donners)])
            fl.write(to_save)

    def add_donner(self, new_donner):
        self._donners.append(new_donner)
        self.save_configs()

    def delete_donner(self, donner_name, delete_all=False):
        if delete_all:
            pass
            self._donners.clear()
        else:
            self._donners.remove(donner_name)
        self.save_configs()

    def init_signals(self):
        @self.client.on_message()
        def get_post(client, message):
            username = message.chat.username
            text = message.text
            print(username, text)



