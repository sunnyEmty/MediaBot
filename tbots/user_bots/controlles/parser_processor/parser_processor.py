from tbots.make_keyboards import KeyboardBuilder
from tbots.interface_bot import InterfaceBot
from aiogram.dispatcher.filters.state import StatesGroup, State


class ContSt(StatesGroup):
    parse = State()
    change_account = State()
    update_api_id = State()
    update_api_hash = State()
    rebuild_bot = State()
    get_phone = State()

    update_checkbox = State()

    update_sources = State()
    edit_sources = State()
    rewrite_sources = State()
    input_sources = State()
    clear_sources = State()

    remove_sources = State()

    append_sources = State()

    parser = State()
    last_state = None


class ParserProcessor(InterfaceBot):
    state = None
    parser = None
    change_account_states = {}

    @staticmethod
    def init_parser_controller(controller_path, parser):
        InterfaceBot._init_configs(controller_path)
        ParserProcessor.parser = parser
        ParserProcessor.set_signals()

    @staticmethod
    def set_signals():
        @InterfaceBot.dp.message_handler(commands=['showp'], state='*')
        async def show_parsing(message):
            while True:
                if ParserProcessor.parser.buff_changed:
                    ParserProcessor.parser.buff_changed = False
                    await InterfaceBot.bot.send_message(message.from_user.id, text=ParserProcessor.parser.buff)


        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'parse', state='*')
        async def parse(message):
            get_media = ParserProcessor.parser.get_media
            power_on = ParserProcessor.parser.power_on
            await InterfaceBot.bot.send_message(message.from_user.id,
                                                text='Что вам нужно?',
                                                reply_markup=KeyboardBuilder.make_parser_kb(get_media, power_on))

# !!!!!!
        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'enable_disable', state='*')
        async def enable_disable(message):
            ParserProcessor.parser.power_on = not ParserProcessor.parser.power_on
            await ParserProcessor.parser.save_configs()
            if not ParserProcessor.parser.power_on:
                ParserProcessor.parser.client.set_parse_mode(None)
            else:
                ParserProcessor.parser.client.set_parse_mode('combined')

            await InterfaceBot.bot.send_message(message.from_user.id,
                                                text='Что вам нужно?',
                                                reply_markup=KeyboardBuilder.make_parser_kb(ParserProcessor.parser.get_media,
                                                                                             ParserProcessor.parser.power_on))

        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'change_account', state='*')
        async def change_account(message):
            await ContSt.change_account.set()
            ParserProcessor.parser.drop_buf()
            text = 'Введите id пользователя.\nЕсли ошиблись Нажмите на \"Отмена\"'

            await InterfaceBot.bot.send_message(message.from_user.id, text=text,
                                                reply_markup=KeyboardBuilder.make_cancel_btn('parse'))
            await ContSt.update_api_id.set()


        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'update_checkbox', state='*')
        async def update_checkbox(message):
            ParserProcessor.parser.get_media = not ParserProcessor.parser.get_media
            await ParserProcessor.parser.save_configs()
            get_media = ParserProcessor.parser.get_media
            power_on = ParserProcessor.parser.power_on
            await InterfaceBot.bot.send_message(message.from_user.id,
                                                text='Что вам нужно?',
                                                reply_markup=KeyboardBuilder.make_parser_kb(get_media,
                                                                                            power_on))

        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'update_sources', state='*')
        async def update_sources(message):

            await InterfaceBot.bot.send_message(message.from_user.id,
                                                text='Что делать с источниками?',
                                                reply_markup=KeyboardBuilder.make_sources_kb())

        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'update_filters', state='*')
        async def update_filters(message):
            await InterfaceBot.bot.send_message(message.from_user.id,
                                                text='Что делать с фильтрами?',
                                                reply_markup=KeyboardBuilder.make_filters_kb())

        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'update_stoplist', state='*')
        async def update_stoplist(message):
            await InterfaceBot.bot.send_message(message.from_user.id,
                                                text='Что делать со стоплистом?',
                                                reply_markup=KeyboardBuilder.make_update_stoplist_kb())
