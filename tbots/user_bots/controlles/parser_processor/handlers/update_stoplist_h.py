from tbots.interface_bot import InterfaceBot
from tbots.user_bots.controlles.parser_processor.parser_processor import ParserProcessor
from tbots.make_keyboards import KeyboardBuilder
from aiogram.dispatcher.filters.state import StatesGroup, State


class StoplistState(StatesGroup):
    input_users = State()
    edit_list = State()


class UpdateStoplistH:
    buf = dict()

    @staticmethod
    def build():
        UpdateStoplistH.update_stoplist_handls()

    @staticmethod
    def update_stoplist_handls():
        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'clear_stoplist', state='*')
        async def clear_stoplist(message):
            ParserProcessor.parser.stop_list = []
            try:
                await ParserProcessor.parser.save_configs()
            except Exception:
                msg = 'Внутренняя ошибка. Повторитие попытку позже'
                await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
            text = 'Успешно\nЧто делать со стоплистом?'
            await InterfaceBot.bot.send_message(message.from_user.id, text=text,
                                                reply_markup=KeyboardBuilder.make_update_stoplist_kb())

        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'print_stoplist', state='*')
        async def print_stoplist(message):
            msg = 'Список пользователей в стоп-листе:\n' + '\n'.join(ParserProcessor.parser.stop_list)
            await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
            await InterfaceBot.bot.send_message(message.from_user.id, text='Что еще нужно?',
                                                reply_markup=KeyboardBuilder.make_update_stoplist_kb())

        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'edit_stoplist', state='*')
        async def edit_stoplist(message):
            msg = 'Введите по одному пользователю в каждой строке.\n Для завершения ввода нажмите /endl'
            await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
            await StoplistState.input_users.set()
            UpdateStoplistH.buf[message.from_user.id] = []
            await InterfaceBot.bot.send_message(message.from_user.id, text='Для отмены нажмите на \"Отмена\"',
                                                reply_markup=KeyboardBuilder.make_cancel_btn('update_stoplist'))

        @InterfaceBot.dp.message_handler(state=StoplistState.input_users)
        async def input_users(message):
            if message.text == '/endl':
                await StoplistState.edit_list.set()
                await message.reply(text='Что хотите сделать?', reply_markup=KeyboardBuilder.make_edit_stoplist_kb())
                return
            if message.text == '/cancel':
                del UpdateStoplistH.buf[message.from_user.id]
                await message.reply(text='Что вам нужно?', reply_markup=KeyboardBuilder.make_update_stoplist_kb())
                return
            if message.text not in UpdateStoplistH.buf[message.from_user.id]:
                UpdateStoplistH.buf[message.from_user.id].append(message.text)

        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'append_users_sl',
                                                state=StoplistState.edit_list)
        async def append_stoplist(message):
            ParserProcessor.parser.add_stoplist(UpdateStoplistH.buf[message.from_user.id])
            try:
                ParserProcessor.parser.add_stoplist(UpdateStoplistH.buf[message.from_user.id])
                await ParserProcessor.parser.save_configs()

            except Exception:
                msg = 'Внутренняя ошибка. Повторитие попытку позже'
                await InterfaceBot.bot.send_message(message.from_user.id, text=msg,
                                                    reply_markup=KeyboardBuilder.make_update_stoplist_kb())
            await InterfaceBot.bot.send_message(message.from_user.id, text='Успешно\nЧто вам нужно?',
                                                reply_markup=KeyboardBuilder.make_update_stoplist_kb())

        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'delete_users_sl',
                                                state=StoplistState.edit_list)
        async def delete_filters(message):
            ParserProcessor.parser.erase_stoplist(UpdateStoplistH.buf[message.from_user.id])
            try:
                await ParserProcessor.parser.save_configs()
            except Exception:
                msg = 'Внутренняя ошибка. Повторитие попытку позже'
                await InterfaceBot.bot.send_message(message.from_user.id, text=msg,
                                                    reply_markup=KeyboardBuilder.make_update_stoplist_kb())
            await InterfaceBot.bot.send_message(message.from_user.id, text='Успешно\nЧто вам нужно?',
                                                reply_markup=KeyboardBuilder.make_update_stoplist_kb())
