from aiogram import types


class KeyboardBuilder:

    @staticmethod
    def make_bots_kb():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Парсер', callback_data='parse'))
        keyboard.add(types.InlineKeyboardButton(text='Постер', callback_data='poster_controller'))
        keyboard.add(types.InlineKeyboardButton(text='Для отправки сообщений', callback_data='sender_controller'))
        return keyboard

    @staticmethod
    def make_parser_kb(take_media, power_on):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Cменить аккаунт юзер-бота', callback_data='change_account'))

        text = 'Забирать медиафайл из сообщения' if not take_media else 'Не забирать медиафайл из сообщения'

        keyboard.add(types.InlineKeyboardButton(text=text, callback_data='update_checkbox'))

        text = 'Включить бота' if not power_on else 'Выключить бота'
        keyboard.add(types.InlineKeyboardButton(text=text, callback_data='enable_disable'))

        keyboard.add(types.InlineKeyboardButton(text='Работа с источниками', callback_data='update_sources'))
        keyboard.add(types.InlineKeyboardButton(text='Работа с фильтрами', callback_data='update_filters'))
        keyboard.add(types.InlineKeyboardButton(text='Работа со стоплистом', callback_data='update_stoplist'))
        keyboard.add(types.InlineKeyboardButton(text='Сообщения администрации', callback_data='update_admin_msg'))

        return keyboard

    @staticmethod
    def make_sources_kb():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Перезаписать источники', callback_data='rewrite_sources'))
        keyboard.add(types.InlineKeyboardButton(text='Отчистить источники', callback_data='clear_sources'))
        keyboard.add(types.InlineKeyboardButton(text='Редактировать источники', callback_data='edit_sources'))
        return keyboard

    @staticmethod
    def make_back_btn():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Отмена', callback_data='parse'))
        return keyboard

