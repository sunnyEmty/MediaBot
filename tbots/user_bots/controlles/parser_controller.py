from tbots.make_keyboards import KeyboardBuilder
from tbots.user_bots.controlles.controller_bot import ControllerBot
from aiogram import executor
from aiogram.dispatcher.filters.state import StatesGroup, State


class ContSt(StatesGroup):
    parse = State()
    change_account = State()
    update_api_id = State()
    update_api_hash = State()

    update_checkbox = State()

    update_sources = State()
    rewrite_sources = State()
    input_sources = State()
    clear_sources = State()

    remove_sources = State()

    append_sources = State()

    parser = State()


class ParserController(ControllerBot):
    state = None
    parser = None
    change_account_states = {}

    @staticmethod
    def init_parser_controller(controller_path, parser):
        ControllerBot._init_configs(controller_path)
        ParserController.parser = parser
        ParserController.set_signals()
        ParserController.change_account_handls()
        ParserController.update_sources_handls()

    @staticmethod
    def set_signals():
        @ControllerBot.dp.message_handler(commands=['showp'])
        async def show_parsing(message):
            while True:
                if ParserController.parser.buff_changed:
                    ParserController.parser.buff_changed = False
                    await ControllerBot.bot.send_message(message.from_user.id, text=ParserController.parser.buff)


        @ControllerBot.dp.callback_query_handler(lambda call: call.data == 'parse')
        async def parse(message):
            get_media = ParserController.parser.get_media
            power_on = ParserController.parser.power_on
            await ControllerBot.bot.send_message(message.from_user.id,
                                                 text='Что вам нужно?',
                                                 reply_markup=KeyboardBuilder.make_parser_kb(get_media, power_on))

# !!!!!!
        @ControllerBot.dp.callback_query_handler(lambda call: call.data == 'enable_disable')
        async def enable_disable(message):
            if ParserController.parser.power_on:
                await ParserController.parser.pause_user_bot()
                ParserController.parser.power_on = False
            else:
                ParserController.parser.run_user_bot()
                ParserController.parser.power_on = True
            get_media = ParserController.parser.get_media
            power_on = ParserController.parser.power_on

            await ControllerBot.bot.send_message(message.from_user.id,
                                                 text='Что вам нужно?',
                                                 reply_markup=KeyboardBuilder.make_parser_kb(get_media,
                                                                                             power_on))

        @ControllerBot.dp.callback_query_handler(lambda call: call.data == 'change_account')
        async def change_account(message):
            await ContSt.change_account.set()
            await ControllerBot.bot.send_message(message.from_user.id, text='Введите id пользователя')
            await ContSt.next()

        @ControllerBot.dp.callback_query_handler(lambda call: call.data == 'update_checkbox')
        async def update_checkbox(message):
            ParserController.parser.get_media = not ParserController.parser.get_media
            ControllerBot.save_configs()
            get_media = ParserController.parser.get_media
            power_on = ParserController.parser.power_on
            await ControllerBot.bot.send_message(message.from_user.id,
                                                 text='Что вам нужно?',
                                                 reply_markup=KeyboardBuilder.make_parser_kb(get_media,
                                                                                             power_on))

        @ControllerBot.dp.callback_query_handler(lambda call: call.data == 'update_sources')
        async def update_sources(message):
            await ControllerBot.bot.send_message(message.from_user.id,
                                                 text='Что делать с источниками?',
                                                 reply_markup=KeyboardBuilder.make_sources_kb())


    @staticmethod
    def change_account_handls():
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
    def update_sources_handls():
        @ControllerBot.dp.callback_query_handler(lambda call: call.data == 'rewrite_sources')
        async def rewrite_sources(message):
            msg = 'Введите чаты (либо имена пользователей, либо ссылки на каналы). ' \
                  'Каждый чат в отдельном сообщении. Когда завиршите ввод - нажмите на кнопку /endl'
            await ControllerBot.bot.send_message(message.from_user.id, text=msg)

            await ContSt.input_sources.set()

        @ControllerBot.dp.message_handler(state=ContSt.input_sources)
        async def input_sources(message):
            try:
                if message.text != '/endl':
                    ParserController.parser.buff['donner'].append(message.text)
                else:
                    ParserController.parser.donners = ParserController.parser.buff['donner'].copy()
                    ParserController.parser.buff['donner'].clear()
                    await ParserController.parser.save_configs()
                    await ControllerBot.bot.send_message(message.from_user.id, text='Список успешно обновлен!!')
                    await ContSt.parser.set()
            except Exception:
                msg = 'Внутренняя ошибка. Повторитие попытку позже'
            await ContSt.input_sources.set()
            return


        @ControllerBot.dp.callback_query_handler(lambda call: call.data == 'clear_sources')
        async def clear_sources(message):
            ParserController.parser.donners.clear()
            await ParserController.parser.save_configs()
            await ControllerBot.bot.send_message(message.from_user.id, text='Удаление прошло успешно')

        @ControllerBot.dp.message_handler(commands=['list'])
        async def update_api_id(message):
            msg = 'Cписок источниоков:\n' + '\n'.join(ParserController.parser.donners)
            await ControllerBot.bot.send_message(message.from_user.id, text=msg)


        @ControllerBot.dp.callback_query_handler(lambda call: call.data == 'edit_sources')
        async def edit_sources(message):

            msg = 'Для вывода списка источников введите /list\n Компнда /app добавляет новые источники. \nКоманда /del ' \
                  'выполняет удаление источников по списку их имен'
            await ControllerBot.bot.send_message(message.from_user.id, text=msg)

        @ControllerBot.dp.message_handler(commands=['del'])
        async def remove_sources(message):
            msg = 'Введите чаты (либо имена пользователей, либо ссылки на каналы). ' \
                  'Каждый чат в отдельном сообщении. Когда завиршите ввод - нажмите на кнопку /endl'
            await ControllerBot.bot.send_message(message.from_user.id, text=msg)
            msg = 'Если ошиблись введите /cancell'
            await ControllerBot.bot.send_message(message.from_user.id, text=msg)
            await ContSt.remove_sources.set()

        @ControllerBot.dp.message_handler(state=ContSt.remove_sources)
        async def remove_cycle(message):
            try:
                if message.text == '/cancell':
                    await ContSt.parser.set()
                    return

                if message.text != '/endl' and message.text in ParserController.parser.donners:

                    ParserController.parser.donners.remove(message.text)
                    ParserController
                else:
                    if message.text == '/endl':
                        await ParserController.parser.save_configs()
                        await ContSt.parser.set()
                        await ControllerBot.bot.send_message(message.from_user.id, text='Удаление прошло успешно')
                    else:
                        await ControllerBot.bot.send_message(message.from_user.id, text='У меня нет такого')

            except Exception:
                msg = 'Внутренняя ошибка. Повторитие попытку позже'
                await ControllerBot.bot.send_message(message.from_user.id, text=msg)
                return


        @ControllerBot.dp.message_handler(commands=['app'])
        async def append_sources(message):
            msg = 'Введите каналы (каждый в отдельном сообщении). Когда завиршите ввод - нажмите на ' \
                  'кнопку /endl.'
            await ControllerBot.bot.send_message(message.from_user.id, text=msg)
            msg = 'Если ошиблись введите /cancell'
            await ControllerBot.bot.send_message(message.from_user.id, text=msg)

            msg = 'ВНИМАНИЕ: Если канал введена не верно - он парсится не будет!!'
            await ControllerBot.bot.send_message(message.from_user.id, text=msg)
            await ContSt.append_sources.set()

        @ControllerBot.dp.message_handler(state=ContSt.append_sources)
        async def app_cycle(message):
            try:
                if message.text == '/cancell':
                    await ContSt.parser.set()
                    return

                if message.text != '/endl':
                    ParserController.parser.buff['donner'].append(message.text)
                else:
                    if message.text == '/endl':
                        ParserController.parser.donners += ParserController.parser.buff['donner']
                        ParserController.parser.buff['donner'].clear()
                        await ParserController.parser.save_configs()
                        await ControllerBot.bot.send_message(message.from_user.id, text='Список успешно обновлен!!')
            except Exception:
                msg = 'Внутренняя ошибка. Повторитие попытку позже'
                await ControllerBot.bot.send_message(message.from_user.id, text=msg)
                return 0


    @staticmethod
    def run():
        executor.start_polling(ControllerBot.dp, skip_updates=True, loop=ParserController.parser.loop, )

