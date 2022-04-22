from tbots.interface_bot import InterfaceBot
from tbots.user_bots.controlles.parser_processor.parser_processor import ParserProcessor
from tbots.make_keyboards import KeyboardBuilder
from aiogram.dispatcher.filters.state import StatesGroup, State


class FilterState(StatesGroup):
    input_filters = State()
    edit_filters = State()
    append_f = State()
    delete_some = State()
    save_st = State()
    dead_st = State()
    cancel_st = State()
    work_with_filters = State()


class UpdateFiltersH:
    buf = {}
    @staticmethod
    def build():
        UpdateFiltersH.update_filters_handls()

    @staticmethod
    def update_filters_handls():
        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'print_filters', state='*')
        async def print_filters(message):
            filts = 'Исползуемые фильтры (записаны в виде регулярного выражения)\n' + ParserProcessor.parser.regular
            await InterfaceBot.bot.send_message(message.from_user.id, text=filts)
            await InterfaceBot.bot.send_message(message.from_user.id,
                                                text='Что вам нужно?',
                                                reply_markup=KeyboardBuilder.make_filters_kb())

        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'clear_filters', state='*')
        async def clear_filters(message):
            ParserProcessor.parser.clear_filters()
            try:
                await ParserProcessor.parser.save_configs()
            except Exception:
                msg = 'Внутренняя ошибка. Повторитие попытку позже'
                await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
            await InterfaceBot.bot.send_message(message.from_user.id, text='Успешно')

        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'work_with_filters', state='*')
        async def work_with_filters(message):
            msg = 'Введите по одному в каждой строке. В качестве фильтра можно использовать нужную последовательность' \
                  'символов, либо регулярное выражение\n Для завершения ввода нажмите /endl, Для отмены нажмите /cancel'

            await InterfaceBot.bot.send_message(message.from_user.id,
                                                text=msg,
                                                reply_markup=KeyboardBuilder.make_input_filters())
            UpdateFiltersH.buf[message.from_user.id] = []
            await FilterState.input_filters.set()

        @InterfaceBot.dp.message_handler(state=FilterState.input_filters)
        async def input_filters(message):
            if message.text == '/endl':
                await FilterState.edit_filters.set()
                await message.reply(text='Что хотите сделать?', reply_markup=KeyboardBuilder.make_edit_filters_kb())
                return
            if message.text == '/cancel':
                del UpdateFiltersH.buf[message.from_user.id]
                await message.reply(text='Что вам нужно?', reply_markup=KeyboardBuilder.make_filters_kb())
                return
            if message.text not in UpdateFiltersH.buf[message.from_user.id]:
                UpdateFiltersH.buf[message.from_user.id].append(message.text)

        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'append_filters',
                                                state=FilterState.edit_filters)
        async def append_filters(message):
            ParserProcessor.parser.add_filters(UpdateFiltersH.buf[message.from_user.id])
            try:
                UpdateFiltersH.app_to_reg(message)
                await ParserProcessor.parser.save_configs()

            except Exception:
                msg = 'Внутренняя ошибка. Повторитие попытку позже'
                await InterfaceBot.bot.send_message(message.from_user.id, text=msg,
                                                    reply_markup=KeyboardBuilder.make_filters_kb())
            await InterfaceBot.bot.send_message(message.from_user.id, text='Успешно\nЧто вам нужно?',
                                                reply_markup=KeyboardBuilder.make_filters_kb())

        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'delete_filters',
                                                state=FilterState.edit_filters)
        async def delete_filters(message):
            ParserProcessor.parser.erase_filters(UpdateFiltersH.buf[message.from_user.id])

            try:
                await ParserProcessor.parser.save_configs()
            except Exception:
                msg = 'Внутренняя ошибка. Повторитие попытку позже'
                await InterfaceBot.bot.send_message(message.from_user.id, text=msg,
                                                    reply_markup=KeyboardBuilder.make_filters_kb())
            await InterfaceBot.bot.send_message(message.from_user.id, text='Успешно\nЧто вам нужно?',
                                                reply_markup=KeyboardBuilder.make_filters_kb())




    @staticmethod
    def app_to_reg(message):
        if not UpdateFiltersH.buf[message.from_user.id]:
            del UpdateFiltersH.buf[message.from_user.id]
            return

        ParserProcessor.parser.add_filters(UpdateFiltersH.buf[message.from_user.id])
        del UpdateFiltersH.buf[message.from_user.id]

