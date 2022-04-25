import asyncio

from tbots.interface_bot import InterfaceBot
from tbots.user_bots.controlles.parser_processor.parser_processor import ParserProcessor, ContSt
from tbots.make_keyboards import KeyboardBuilder
from tbots.bot_exeoptions import UserConnectionException
from pyrogram import Client
from pyrogram.errors.exceptions.flood_420 import FloodWait
import re


class ChangeAccountH:
    @staticmethod
    def build():
        ChangeAccountH.change_account_handls()

    @staticmethod
    def change_account_handls():

        @InterfaceBot.dp.message_handler(state=ContSt.update_api_id)
        async def update_api_id(message):
            ParserProcessor.parser.buff['api_id'] = message.text
            msg = 'Введите api_hash'
            await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
            await ContSt.update_api_hash.set()

        @InterfaceBot.dp.message_handler(state=ContSt.update_api_hash)
        async def update_api_hash(message):
            ParserProcessor.parser.buff['api_hash'] = message.text
            msg = 'Введите номер телефона привязанный к аккаунту'
            await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
            await ContSt.get_phone.set()

        @InterfaceBot.dp.message_handler(state=ContSt.get_phone)
        async def send_key(message):
            ParserProcessor.parser.buff['phone'] = message.text
            sender = None
            while True:
                try:
                    sender = Client(
                        'sender',
                        api_id=ParserProcessor.parser.buff['api_id'],
                        api_hash=ParserProcessor.parser.buff['api_hash'],
                        phone_number=ParserProcessor.parser.buff['phone']
                    )
                    await sender.connect()
                    await sender.send_code(ParserProcessor.parser.buff['phone'])

                except FloodWait as f:
                    msg = 'Ожидайте ' + str(f.x) + ' секунд или нажмите на кнопку "Отмена"'
                    await InterfaceBot.bot.send_message(text=msg,
                                                        reply_markup=KeyboardBuilder.make_cancel_btn('change_account'))
                    await asyncio.sleep(f.x)
                except Exception:
                    msg = 'Введенные данные не корректны. Повторите их ввод.\n Введите апи айди'
                    await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
                    await ContSt.update_api_id.set()
                    return
                else:
                    msg = 'Успешно\nВведите код подтверждения пришедший на введенный номер'
                    await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
                    await ContSt.rebuild_bot.set()
                    return


        @InterfaceBot.dp.message_handler(state=ContSt.rebuild_bot)
        async def rebuild_bot(message):
            ParserProcessor.parser.buff['password'] = message.text
            try:
                await ParserProcessor.parser.save_configs()
            except Exception:
                msg = 'Ошибка, код не действителен. Повторите ввод кода'
                await InterfaceBot.bot.send_message(message.from_user.id, text=msg)
                name = 'Отправить код повторно'
                kb = KeyboardBuilder.make_btn(text=name, callback_data='resend_key')
                await InterfaceBot.bot.send_message('Можете также', reply_markup=kb)
            else:
                get_media = ParserProcessor.parser.get_media
                power_on = ParserProcessor.parser.power_on
                await InterfaceBot.bot.send_message(message.from_user.id, text='Настройки успешно сохранены!!',
                                                    reply_markup=KeyboardBuilder.make_parser_kb(get_media, power_on))

        @InterfaceBot.dp.callback_query_handler(lambda call: call.data == 'resend_key', state='*')
        async def resend_key(message):
            sender = Client(
                'sender',
                api_id=ParserProcessor.parser.buff['api_id'],
                api_hash=ParserProcessor.parser.buff['api_hash'],
                phone_number=ParserProcessor.parser.buff['phone']
            )
            await sender.connect()
            await sender.send_code(ParserProcessor.parser.buff['phone'])
            ContSt.rebuild_bot.set()
            await InterfaceBot.bot.send_message('Введите код')

