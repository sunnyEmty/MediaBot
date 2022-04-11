from telebot import types


class KeyboardBuilder:

    @staticmethod
    def make_bots_keyboard():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Парсер', callback_data='parse'))
        keyboard.add(types.InlineKeyboardButton(text='Постер', callback_data='poster_controller'))
        keyboard.add(types.InlineKeyboardButton(text='Для отправки сообщений', callback_data='sender_controller'))
        return keyboard

    @staticmethod
    def make_parser_keyboard(take_media):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Cменить аккаунт юзер-бота', callback_data='change_account'))

        text = 'Забирать медиафайл из сообщения' if not take_media else 'Не забирать медиафайл из сообщения'

        keyboard.add(types.InlineKeyboardButton(text=text, callback_data='update_checkbox'))
        keyboard.add(types.InlineKeyboardButton(text='Работа с источниками', callback_data='update_sources'))
        keyboard.add(types.InlineKeyboardButton(text='Работа с фильтрами', callback_data='update_filters'))
        keyboard.add(types.InlineKeyboardButton(text='Работа со стоплистом', callback_data='update_stoplist'))
        keyboard.add(types.InlineKeyboardButton(text='Сообщения администрации', callback_data='update_admin_msg'))

        return keyboard

