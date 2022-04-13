from tbots.make_keyboards import KeyboardBuilder
from tbots.user_bots.controlles.controller_bot import ControllerBot
from tbots.user_bots.controlles.states import ChangeAccountSts
from aiogram import executor


class ParserController(ControllerBot):

    parser = None
    change_account_states = {}

    @staticmethod
    def init_parser_controller(controller_path, parser):
        ControllerBot._init_configs(controller_path)
        ParserController.parser = parser
        ParserController.change_account_states = {
            'state': ChangeAccountSts.WAITING_API_ID,
            ChangeAccountSts.WAITING_API_ID:ParserController.update_api_id,

        }
        ParserController.set_signals()

    @staticmethod
    def set_signals():

        @ControllerBot.dp.callback_query_handler(lambda call: call.data == 'parse')
        async def parse(message):
            await ControllerBot.bot.send_message(message.from_user.id,
                                                 text='Что вам нужно?',
                                                 reply_markup=KeyboardBuilder.make_parser_keyboard(ControllerBot.check_box))

        @ControllerBot.dp.callback_query_handler(lambda call: call.data == 'change_account')
        async def change_account(message):
            msg = ControllerBot.dp.send_message(message.from_user.id, text='Введите id пользователя')
            next_handler = ParserController.change_account_states[ParserController.change_account_states['state']]
            await ControllerBot.bot.register_next_step_handler(msg, next_handler)

    @staticmethod
    def update_api_id(msg):
        try:
            new_api_id = msg.text

        except Exception:
            pass

    @staticmethod
    def run():
        executor.start_polling(ControllerBot.dp, skip_updates=True, loop=ParserController.parser.loop)









