from tbots.interface_bot import InterfaceBot
from tbots.user_bots.controlles.parser_processor.parser_processor import ParserProcessor, ContSt


class UpdateFiltersH:
    @staticmethod
    def build():
        UpdateFiltersH.update_filters_handls()

    @staticmethod
    def update_filters_handls():
        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'clear_filters')
        async def clear_filters(message):
            ParserProcessor.parser.regular = '.*'
            await ParserProcessor.parser.save_configs()
            await InterfaceBot.bot.send_message(message.from_user.id, text='Успешно')

        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'edit_filters')
        async def edit_filters(message):
            msg = 'Для вывода списка фильтров введите /list\n Компнда /app добавляет новые источники. \nКоманда /del ' \
                  'выполняет удаление источников по списку их имен'
            await InterfaceBot.bot.send_message(message.from_user.id, text=msg)

