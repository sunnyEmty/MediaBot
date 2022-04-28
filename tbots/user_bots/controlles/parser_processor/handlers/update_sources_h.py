import pyrogram.errors

from tbots.interface_bot import InterfaceBot
from tbots.user_bots.controlles.parser_processor.parser_processor import ParserProcessor, ContSt
from tbots.make_keyboards import KeyboardBuilder
from tbots.bot_exeoptions import DonnerNameException
import re

class UpdateSourcesH:
    @staticmethod
    def build():
        UpdateSourcesH.update_sources_handls()

    @staticmethod
    def update_sources_handls():
        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'rewrite_sources', state='*')
        async def rewrite_sources(message):
            msg = 'Введите имена чатов. ' \
                  'Каждый чат в отдельном сообщении. Когда завиршите ввод - нажмите на кнопку /endl'
            await InterfaceBot.bot.send_message(message.from_user.id, text=msg,
                                                reply_markup=KeyboardBuilder.make_cancel_btn('update_sources'))
            ParserProcessor.parser.buff['donner'] = []
            await ContSt.append_sources.set()

        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'clear_sources', state='*')
        async def clear_sources(message):
            ParserProcessor.parser.donners.clear()
            await ParserProcessor.parser.save_configs()
            await InterfaceBot.bot.send_message(message.from_user.id, text='Удаление прошло успешно')

        @InterfaceBot.dp.message_handler(commands=['list'], state=ContSt.edit_sources)
        async def sources(message):
            msg = 'Cписок источниоков:\n' + '\n'.join(ParserProcessor.parser.donners)
            await InterfaceBot.bot.send_message(message.from_user.id, text=msg)

        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'edit_sources', state='*')
        async def edit_sources(message):
            await ContSt.edit_sources.set()
            msg = 'Для вывода списка источников введите /list\n Компнда /app добавляет новые источники. \nКоманда /del ' \
                  'выполняет удаление источников по списку их имен'
            ParserProcessor.parser.buff['donner'] = []
            await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
            await InterfaceBot.bot.send_message(message.from_user.id, text='Что вам нужно?',
                                                reply_markup=KeyboardBuilder.make_cancel_btn('update_sources'))

        @InterfaceBot.dp.message_handler(commands=['del'], state=ContSt.edit_sources)
        async def remove_sources(message):
            msg = 'Введите имена чатов. ' \
                  'Каждый чат в отдельном сообщении. Когда завиршите ввод - нажмите на /endl'
            await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
            msg = 'Если ошиблись введите \"Отмена\"'
            await InterfaceBot.bot.send_message(message.from_user.id, text=msg,
                                                reply_markup=KeyboardBuilder.make_cancel_btn('edit_sources'))
            await ContSt.remove_sources.set()


        @InterfaceBot.dp.message_handler(state=ContSt.remove_sources)
        async def remove_cycle(message):
            try:

                if message.text != '/endl' and message.text in ParserProcessor.parser.donners:
                    ParserProcessor.parser.buff['donner'].append(message.text)
                else:
                    if message.text == '/endl':

                        for donner in ParserProcessor.parser.buff['donner']:
                            ParserProcessor.parser.donners.remove(donner)


                        await ParserProcessor.parser.save_configs()
                        await ContSt.parser.set()
                        await InterfaceBot.bot.send_message(message.from_user.id, text='Удаление прошло успешно',
                                                            reply_markup=KeyboardBuilder.make_sources_kb())
                    else:
                        await InterfaceBot.bot.send_message(message.from_user.id, text='У меня нет такого')
            except Exception:
                msg = 'Внутренняя ошибка. Повторитие попытку позже'
                await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
                return

        @InterfaceBot.dp.message_handler(commands=['app'], state=ContSt.edit_sources)
        async def append_sources(message):
            msg = 'Введите каналы (каждый в отдельном сообщении). Когда завиршите ввод - нажмите на ' \
                  'кнопку /endl.'
            await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
            msg = 'Если ошиблись - нажмите \"Отмена\"'
            await InterfaceBot.bot.send_message(message.from_user.id, text=msg,
                                                reply_markup=KeyboardBuilder.make_cancel_btn('edit_sources'))

            msg = 'ВНИМАНИЕ: Если канал введена не верно - он парсится не будет!!'
            await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
            await ContSt.append_sources.set()
            ParserProcessor.parser.buff['donner'] = ParserProcessor.parser.donners

        @InterfaceBot.dp.message_handler(state=ContSt.append_sources)
        async def app_cycle(message):
            try:
                if message.text != '/endl':
                    if message.text not in ParserProcessor.parser.buff['donner']:
                        await ParserProcessor.parser.client.join_chat(message.text)
                        ParserProcessor.parser.buff['donner'].append(message.text)

                else:
                    ParserProcessor.parser.donners = ParserProcessor.parser.buff['donner']
                    await ParserProcessor.parser.save_configs()
                    await InterfaceBot.bot.send_message(message.from_user.id, text='Список успешно обновлен!!',
                                                        reply_markup=KeyboardBuilder.make_sources_kb())
                    ParserProcessor.parser.buff['donner'].clear()
            except pyrogram.errors.BadRequest:
                msg = 'Канал не найден (возможно его не существует)'
                await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
            except Exception:
                msg = 'Внутренняя ошибка. Повторитие попытку позже'
                await InterfaceBot.bot.send_message(message.from_user.id, text=msg)

