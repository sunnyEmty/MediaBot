from tbots.controll_bot.controll_bot import controller_bot
from tbots.user_bots.parser_bot.parser import Parser
import asyncio


async def parser_updater_t():
    await parser_bot.run()


async def controller_updater_t():

    await controller_bot.polling(none_stop=True, interval=0)



def create_tasks():
    main_loop.create_task(parser_updater_t())
    main_loop.create_task(controller_updater_t())


if __name__ == '__main__':

    parser_bot = Parser(path='C:/Users/User/PycharmProjects/MediaBot/tbots/user_bots/parser_bot/config.ini')

    main_loop = asyncio.get_event_loop()
    create_tasks()
    main_loop.run_forever()
