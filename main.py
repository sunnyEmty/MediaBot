from tbots.user_bots.controlles.parser_controller import ParserController
from tbots.user_bots.parser_bot.parser import Parser
import asyncio

'''
async def parser_updater_t():
    parser_bot.run()


async def controller_updater_t():

    await ParserController.bot.polling(none_stop=True, interval=0)



def create_tasks():
    main_loop.create_task(parser_updater_t())
    main_loop.create_task(controller_updater_t())

'''
if __name__ == '__main__':

    ParserController.init_parser_controller(controller_path='tbots/control_bot_configs.json',
                                            parser=Parser('tbots/user_bots/parser_bot/config.ini'))
    ParserController.run()

'''
    main_loop = asyncio.get_event_loop()
    create_tasks()
    main_loop.run_forever()
'''
