from tbots.interface_bot import InterfaceBot
from tbots.user_bots.controlles.parser_processor.parser_processor import ParserProcessor
from tbots.make_keyboards import KeyboardBuilder
from aiogram.dispatcher.filters.state import StatesGroup, State


class FilterState(StatesGroup):
    app_filters = State()
    edit_filters = State()
    save_st = State()
    dead_st = State()
    cancel_st = State()


class UpdateFiltersH:
    buf = {}
    @staticmethod
    def build():
        UpdateFiltersH.update_filters_handls()

    @staticmethod
    def update_filters_handls():
        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'print_filters')
        async def print_filters(message):
            filts = 'Исползуемые фильтры (записаны в виде регулярного выражения)\n' + ParserProcessor.parser.regular
            await InterfaceBot.bot.send_message(message.from_user.id, text=filts)
            await InterfaceBot.bot.send_message(message.from_user.id,
                                                text='Что вам нужно?',
                                                reply_markup=KeyboardBuilder.make_filters_kb())

        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'clear_filters')
        async def clear_filters(message):
            ParserProcessor.parser.regular = '.*'
            try:
                await ParserProcessor.parser.save_configs()
            except Exception:
                msg = 'Внутренняя ошибка. Повторитие попытку позже'
                await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
            await InterfaceBot.bot.send_message(message.from_user.id, text='Успешно')

        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'edit_filters')
        async def edit_filters(message):
            await FilterState.edit_filters.set()
            await InterfaceBot.bot.send_message(message.from_user.id,
                                                text='Что вам нужно?',
                                                reply_markup=KeyboardBuilder.make_edit_filters_kb())



        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'append_filters', state=FilterState.edit_filters)
        async def append_filters(message):
            msg = 'Введите по одному в каждой строке. В качестве фильтра можно использовать нужную последовательность' \
                  'символов, либо регулярное выражение\n Для завершения ввода нажмите /save, Для отмены нажмите /cancel'

            await InterfaceBot.bot.send_message(message.from_user.id,
                                                text=msg,
                                                reply_markup=KeyboardBuilder.make_append_filters())
            UpdateFiltersH.buf[message.from_user.id] = []
            await FilterState.app_filters.set()

        @InterfaceBot.dp.message_handler(state=FilterState.app_filters)
        async def append(message):
            if message.text == '/save':
                await FilterState.edit_filters.set()
                try:
                    await UpdateFiltersH.save(message)
                except:
                    msg = 'Внутренняя ошибка. Повторитие попытку позже'
                    await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
                await message.reply(text='Успешно\nЧто вам нужно?', reply_markup=KeyboardBuilder.make_edit_filters_kb())
                return
            if message.text == '/cancel':
                await FilterState.edit_filters.set()
                del UpdateFiltersH.buf[message.from_user.id]
                await message.reply(text='Что вам нужно?', reply_markup=KeyboardBuilder.make_edit_filters_kb())
                return
            UpdateFiltersH.buf[message.from_user.id].append(message.text)

        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'delete_filters')
        async def delete_filters(message):
            pass

    @staticmethod
    async def save(message):
        new_part = '|'.join(UpdateFiltersH.buf[message.from_user.id])
        if ParserProcessor.parser.regular != '.*':
            ParserProcessor.parser.regular = '|'.join([ParserProcessor.parser.regular, new_part])
        else:
            ParserProcessor.parser.regular = new_part

        del UpdateFiltersH.buf[message.from_user.id]

