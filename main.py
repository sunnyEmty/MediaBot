from tbots.user_bots.controlles.parser_controller import ParserController
from tbots.user_bots.parser_bot.parser import Parser
from aiogram import executor

if __name__ == '__main__':

    ParserController.init_parser_controller(controller_path='tbots/control_bot_configs.json',
                                            parser=Parser('tbots/user_bots/parser_bot/config.ini'))
    ParserController.run()

