from tbots.user_bots.controlles.parser_processor.parser_processor import ParserProcessor
from tbots.interface_bot import InterfaceBot
from tbots.user_bots.parser_bot.parser import Parser
from tbots.user_bots.controlles.parser_processor.handlers.change_account_h import ChangeAccountH
from tbots.user_bots.controlles.parser_processor.handlers.update_filters_h import UpdateFiltersH
from tbots.user_bots.controlles.parser_processor.handlers.update_sources_h import UpdateSourcesH
from tbots.user_bots.controlles.parser_processor.handlers.update_stoplist_h import UpdateStoplistH
from tbots.user_bots.user_bot import UserBot
from aiogram import executor


def init_system():
    controller_path = 'tbots/control_bot_configs.json'
    parser = Parser('tbots/user_bots/parser_bot/config.ini')

    ParserProcessor.init_parser_controller(controller_path=controller_path, parser=parser)
    ChangeAccountH.build()
    UpdateFiltersH.build()
    UpdateSourcesH.build()
    UpdateStoplistH.build()


if __name__ == '__main__':
    init_system()
    executor.start_polling(InterfaceBot.dp, skip_updates=True, loop=UserBot.loop)
