from tbots.make_keyboards import KeyboardBuilder
from tbots.user_bots.controlles.controller_bot import ControllerBot
from aiogram import executor
from aiogram.dispatcher.filters.state import StatesGroup, State


class ContSt(StatesGroup):
    change_account = State()
    update_api_id = State()
    update_api_hash = State()



class ParserController(ControllerBot):
    state = None
    parser = None
    change_account_states = {}



    @staticmethod
    def init_parser_controller(controller_path, parser):
        ControllerBot._init_configs(controller_path)
        ParserController.parser = parser
        ParserController.set_signals()
        ParserController.set_change_account_handlers()

    @staticmethod
    def set_signals():

        @ControllerBot.dp.callback_query_handler(lambda call: call.data == 'parse')
        async def parse(message):
            await ControllerBot.bot.send_message(message.from_user.id,
                                                 text='Что вам нужно?',
                                                 reply_markup=KeyboardBuilder.make_parser_keyboard(ControllerBot.check_box))

        @ControllerBot.dp.callback_query_handler(lambda call: call.data == 'change_account')
        async def change_account(message):
            await ContSt.change_account.set()
            await ControllerBot.bot.send_message(message.from_user.id, text='Введите id пользователя')
            await ContSt.next()





    @staticmethod
    def set_change_account_handlers():
        @ControllerBot.dp.message_handler(state=ContSt.update_api_id)
        async def update_api_id(message):
            try:
                new_api_id = int(message.text)
            except ValueError:
                msg = 'Входные данные не корректны введите api id еще раз'
                await ControllerBot.bot.send_message(message.from_user.id, text=msg)
                return
            ParserController.parser.buff['api_id'] = new_api_id
            msg = 'Введите api_hash'
            await ControllerBot.bot.send_message(message.from_user.id, text=msg)
            await ContSt.next()

        @ControllerBot.dp.message_handler(state=ContSt.update_api_hash)
        async def update_api_hash(message):
            ParserController.parser.buff['api_hash'] = message.text

            try:
                ParserController.parser.save_configs()
            except Exception:
                msg = 'Внутренняя ошибка. Повторитие попытку позже'
                await ControllerBot.bot.send_message(message.from_user.id, text=msg)
            await ControllerBot.bot.send_message(message.from_user.id, text='Настройки успешно сохранены!!')






    @staticmethod
    def run():
        executor.start_polling(ControllerBot.dp, skip_updates=True, loop=ParserController.parser.loop)









