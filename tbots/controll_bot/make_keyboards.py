from telebot import types


class KeyboardBuilder:

    @staticmethod
    def make_bots_keyboard():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Парсер', callback_data='parser_controller'))
        keyboard.add(types.InlineKeyboardButton(text='Постер', callback_data='poster_controller'))
        keyboard.add(types.InlineKeyboardButton(text='Для отправки сообщений', callback_data='sender_controller'))
        return keyboard

    @staticmethod
    def make_parser_keyboard():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Cменить аккаунт юзер-бота', callback_data='parser_controller'))
        keyboard.add(types.InlineKeyboardButton(text='Постер', callback_data='poster_controller'))
        keyboard.add(types.InlineKeyboardButton(text='Для отправки сообщений', callback_data='sender_controller'))

        return keyboard
