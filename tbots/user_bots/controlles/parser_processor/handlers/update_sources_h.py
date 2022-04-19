from tbots.interface_bot import InterfaceBot
from tbots.user_bots.controlles.parser_processor.parser_processor import ParserProcessor, ContSt


class UpdateSourcesH:
    @staticmethod
    def build():
        UpdateSourcesH.update_sources_handls()

    @staticmethod
    def update_sources_handls():
        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'rewrite_sources')
        async def rewrite_sources(message):
            msg = 'Введите имена чатов. ' \
                  'Каждый чат в отдельном сообщении. Когда завиршите ввод - нажмите на кнопку /endl'
            await InterfaceBot.bot.send_message(message.from_user.id, text=msg)

            await ContSt.input_sources.set()

        @InterfaceBot.dp.message_handler(state=ContSt.input_sources)
        async def input_sources(message):
            try:
                if message.text != '/endl':
                    ParserProcessor.parser.buff['donner'].append(message.text)
                else:
                    ParserProcessor.parser.donners = ParserProcessor.parser.buff['donner'].copy()
                    ParserProcessor.parser.buff['donner'].clear()
                    await ParserProcessor.parser.save_configs()
                    await InterfaceBot.bot.send_message(message.from_user.id, text='Список успешно обновлен!!')
                    await ContSt.parser.set()
            except Exception:
                msg = 'Внутренняя ошибка. Повторитие попытку позже'
            await ContSt.input_sources.set()
            return

        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'clear_sources')
        async def clear_sources(message):
            ParserProcessor.parser.donners.clear()
            await ParserProcessor.parser.save_configs()
            await InterfaceBot.bot.send_message(message.from_user.id, text='Удаление прошло успешно')

        @InterfaceBot.dp.message_handler(commands=['list'])
        async def sources(message):
            msg = 'Cписок источниоков:\n' + '\n'.join(ParserProcessor.parser.donners)
            await InterfaceBot.bot.send_message(message.from_user.id, text=msg)

        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'edit_sources')
        async def edit_sources(message):

            msg = 'Для вывода списка источников введите /list\n Компнда /app добавляет новые источники. \nКоманда /del ' \
                  'выполняет удаление источников по списку их имен'
            await InterfaceBot.bot.send_message(message.from_user.id, text=msg)

        @InterfaceBot.dp.message_handler(commands=['del'])
        async def remove_sources(message):
            msg = 'Введите имена чатов. ' \
                  'Каждый чат в отдельном сообщении. Когда завиршите ввод - нажмите на кнопку /endl'
            await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
            msg = 'Если ошиблись введите /cancell'
            await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
            await ContSt.remove_sources.set()

        @InterfaceBot.dp.message_handler(state=ContSt.remove_sources)
        async def remove_cycle(message):
            try:
                if message.text == '/cancell':
                    await ContSt.parser.set()
                    return

                if message.text != '/endl' and message.text in ParserProcessor.parser.donners:

                    ParserProcessor.parser.donners.remove(message.text)
                    ParserProcessor
                else:
                    if message.text == '/endl':
                        await ParserProcessor.parser.save_configs()
                        await ContSt.parser.set()
                        await InterfaceBot.bot.send_message(message.from_user.id, text='Удаление прошло успешно')
                    else:
                        await InterfaceBot.bot.send_message(message.from_user.id, text='У меня нет такого')

            except Exception:
                msg = 'Внутренняя ошибка. Повторитие попытку позже'
                await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
                return

        @InterfaceBot.dp.message_handler(commands=['app'])
        async def append_sources(message):
            msg = 'Введите каналы (каждый в отдельном сообщении). Когда завиршите ввод - нажмите на ' \
                  'кнопку /endl.'
            await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
            msg = 'Если ошиблись введите /cancell'
            await InterfaceBot.bot.send_message(message.from_user.id, text=msg)

            msg = 'ВНИМАНИЕ: Если канал введена не верно - он парсится не будет!!'
            await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
            await ContSt.append_sources.set()

        @InterfaceBot.dp.message_handler(state=ContSt.append_sources)
        async def app_cycle(message):
            try:
                if message.text == '/cancell':
                    await ContSt.parser.set()
                    return

                if message.text != '/endl':
                    ParserProcessor.parser.buff['donner'].append(message.text)
                else:
                    if message.text == '/endl':
                        ParserProcessor.parser.donners += ParserProcessor.parser.buff['donner']
                        ParserProcessor.parser.buff['donner'].clear()
                        await ParserProcessor.parser.save_configs()
                        await InterfaceBot.bot.send_message(message.from_user.id, text='Список успешно обновлен!!')
            except Exception:
                msg = 'Внутренняя ошибка. Повторитие попытку позже'
                await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
                return 0
