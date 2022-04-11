from tbots.make_keyboards import KeyboardBuilder
from tbots.user_bots.controlles.controller_bot import ControllerBot
from tbots.user_bots.controlles.states import ChangeAccountSts
import asyncio


class ParserController(ControllerBot):

    parser = None
    change_account_states = {}

    @staticmethod
    def init_parser_controller(controller_path, parser):
        ControllerBot._init_configs(controller_path)
        ParserController.parser = parser
        ParserController.change_account_states = {
            'state':ChangeAccountSts.WAITING_API_ID,
            ChangeAccountSts.WAITING_API_ID:ParserController.update_api_id,

        }
        ParserController.set_signals()
        ParserController.login()

    @staticmethod
    def login():
        ParserController.parser.user_bot.start()
        ParserController.parser.user_bot.stop()

    @staticmethod
    def set_signals():

        @ControllerBot.bot.callback_query_handler(func=lambda call: call.data == 'parse')
        def parse(message):
            ControllerBot.bot.send_message(message.from_user.id,
                                  text='Что вам нужно?',
                                  reply_markup=KeyboardBuilder.make_parser_keyboard(ControllerBot.check_box))

        @ControllerBot.bot.callback_query_handler(func=lambda call: call.data == 'change_account')
        def change_account(message):
            msg = ControllerBot.bot.send_message(message.from_user.id, text='Введите id пользователя')
            next_handler = ParserController.change_account_states[ParserController.change_account_states['state']]
            ControllerBot.bot.register_next_step_handler(msg, next_handler)




    @staticmethod
    def update_api_id(msg):
        try:
            new_api_id = msg.text

        except Exception:
            pass

    @staticmethod
    async def _run_parser():
        await ParserController.parser.user_bot.start()

    @staticmethod
    def _finish_parser():
        ParserController.parser.user_bot.stop()


    @staticmethod
    async def _run_controller():
        ParserController.bot.polling(none_stop=True, interval=0)


    @staticmethod
    def run():
        main_loop = asyncio.get_event_loop()
        main_loop.create_task(ParserController._run_parser())
        main_loop.create_task(ParserController._run_controller())
        main_loop.run_forever()









