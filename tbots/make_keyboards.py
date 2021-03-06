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
        keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back_to_main'))
        return keyboard

    @staticmethod
    def make_sources_kb():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Перезаписать источники', callback_data='rewrite_sources'))
        keyboard.add(types.InlineKeyboardButton(text='Отчистить источники', callback_data='clear_sources'))
        keyboard.add(types.InlineKeyboardButton(text='Редактировать источники', callback_data='edit_sources'))
        keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='parse'))
        return keyboard

    @staticmethod
    def make_cancel_btn(callback_data):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Отмена', callback_data=callback_data))
        return keyboard

    @staticmethod
    def make_filters_kb():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Удалить все фильтры', callback_data='clear_filters'))
        keyboard.add(types.InlineKeyboardButton(text='Добавить/удалить фильтры', callback_data='work_with_filters'))
        adds = ' (в виде регулярного выражения)'
        keyboard.add(types.InlineKeyboardButton(text='Вывод фильтров' + adds, callback_data='print_filters'))
        keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='parse'))
        return keyboard

    @staticmethod
    def make_edit_filters_kb():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Добавить фильтры', callback_data='append_filters'))
        keyboard.add(types.InlineKeyboardButton(text='Выборочно удалить фильтры', callback_data='delete_filters'))
        keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='update_filters'))
        return keyboard

    @staticmethod
    def make_input_filters():
        keyboard = types.ReplyKeyboardMarkup()
        keyboard.add(types.KeyboardButton(text='/endl'))
        return keyboard

    @staticmethod
    def make_update_stoplist_kb():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Отчистить стоплист', callback_data='clear_stoplist'))
        keyboard.add(types.InlineKeyboardButton(text='Добавить/удалить пользователей', callback_data='edit_stoplist'))
        keyboard.add(types.InlineKeyboardButton(text='Вывести стоплист', callback_data='print_stoplist'))
        keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='parse'))
        return keyboard

    @staticmethod
    def make_edit_stoplist_kb():
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Добавить пользователей', callback_data='append_users_sl'))
        keyboard.add(types.InlineKeyboardButton(text='Удалить', callback_data='delete_users_sl'))
        keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='update_stoplist'))
        return keyboard

    @staticmethod
    def make_btn(text, callback_data):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text=text, callback_data=callback_data))
        return keyboard
