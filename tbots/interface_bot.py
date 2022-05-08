import json
from tbots.make_keyboards import KeyboardBuilder
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


class InterfaceBot:
    token = None
    bot = None
    path = None
    dp = None

    @staticmethod
    def _init_configs(path):
        with open(path, 'r', encoding='utf-8') as f:
            res = json.load(f)
            res = json.loads(res)
            InterfaceBot.token = res['token']
            InterfaceBot.bot = Bot(token=InterfaceBot.token)
            InterfaceBot.path = path

        InterfaceBot.dp = Dispatcher(InterfaceBot.bot, storage=MemoryStorage())
        InterfaceBot.set_start_signals()

    @staticmethod
    def save_configs():
        json_str = json.dumps(
            {
                'token': InterfaceBot.token,
            }
        )
        with open(InterfaceBot.path, 'w', encoding='utf-8') as f:
            json.dump(json_str, f)

    @staticmethod
    def set_start_signals():
        @InterfaceBot.dp.message_handler(commands=['start'], state='*')
        async def get_start_msg(message):
            await InterfaceBot.bot.send_message(message.from_user.id,
                                                text='Выбери нужного бота.',
                                                reply_markup=KeyboardBuilder.make_bots_kb())

        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'back_to_main', state='*')
        async def back_to_main(message):
            await InterfaceBot.bot.send_message(message.from_user.id,
                                                text='Выбери нужного бота.',
                                                reply_markup=KeyboardBuilder.make_bots_kb())
