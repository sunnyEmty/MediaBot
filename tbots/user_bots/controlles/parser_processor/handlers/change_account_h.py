from tbots.interface_bot import InterfaceBot
from tbots.user_bots.controlles.parser_processor.parser_processor import ParserProcessor, ContSt
class ChangeAccountH:
    @staticmethod
    def build():
        ChangeAccountH.change_account_handls()

    @staticmethod
    def change_account_handls():
        @InterfaceBot.dp.message_handler(state=ContSt.update_api_id)
        async def update_api_id(message):
            try:
                new_api_id = int(message.text)

            except ValueError:
                msg = 'Входные данные не корректны введите api id еще раз'
                await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
                return
            ParserProcessor.parser.buff['api_id'] = new_api_id
            msg = 'Введите api_hash'
            await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
            await ContSt.next()

        @InterfaceBot.dp.message_handler(state=ContSt.update_api_hash)
        async def update_api_hash(message):
            ParserProcessor.parser.buff['api_hash'] = message.text

            try:
                ParserProcessor.parser.save_configs()
            except Exception:
                msg = 'Внутренняя ошибка. Повторитие попытку позже'
                await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
            await InterfaceBot.bot.send_message(message.from_user.id, text='Настройки успешно сохранены!!')
