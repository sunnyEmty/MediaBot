import json
from tbots.make_keyboards import KeyboardBuilder
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

class ControllerBot:
    token = None
    check_box = None
    power_on = None
    bot = None
    path = None
    dp = None

    @staticmethod
    def _init_configs(path):
        with open(path, 'r', encoding='utf-8') as f:
            res = json.load(f)
            res = json.loads(res)
            ControllerBot.token = res['token']
            ControllerBot.check_box = res['check_box']
            ControllerBot.bot = Bot(token=ControllerBot.token)
            ControllerBot.path = path
        ControllerBot.dp = Dispatcher(ControllerBot.bot, storage=MemoryStorage())
        ControllerBot.set_start_signals()

    @staticmethod
    def save_configs():
        json_str = json.dumps(
            {
                'token': ControllerBot.token,
                'check_box': ControllerBot.check_box,
            }
        )
        with open(ControllerBot.path, 'w', encoding='utf-8') as f:
            json.dump(json_str, f)

    @staticmethod
    def set_start_signals():

        @ControllerBot.dp.message_handler(commands=['start'])
        async def get_start_msg(message):
            await ControllerBot.bot.send_message(message.from_user.id,
                                                 text='Выбери нужного бота.',
                                                 reply_markup=KeyboardBuilder.make_bots_kb())





        '''
        @self.bot.callback_query_handler(func=lambda call: call.data == 'change_account')
        def change_account(message):
            msg = self.bot.send_message(message.from_user.id,
                                               text='Введите id пользователя')
            self.bot.register_next_step_handler(msg,)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'update_checkbox')
        def update_checkbox(message):
            pass

        @self.bot.callback_query_handler(func=lambda call: call.data == 'update_sources')
        def update_sources(message):
            pass

        @self.bot.callback_query_handler(func=lambda call: call.data == 'update_filters')
        def update_filters(message):
            pass

        @self.bot.callback_query_handler(func=lambda call: call.data == 'update_stoplist')
        def update_stoplist(message):
            pass

        @self.bot.callback_query_handler(func=lambda call: call.data == 'update_admin_msg')
        def update_admin_msg(message):
            pass
        '''
