from tbots.user_bots.controlles.parser_controller import ParserController
from tbots.make_keyboards import KeyboardBuilder
from tbots.user_bots.controlles.controller_bot import ControllerBot

CONTROL_BOT = ControllerBot._init_configs('tbots/control_bot_configs.json')


@ControllerBot.bot.message_handler(commands=['start'])
def get_start_msg(message):
    ControllerBot.bot.send_message(message.from_user.id,
                                 text='Выбери нужного бота.',
                                 reply_markup=KeyboardBuilder.make_bots_keyboard())


@ControllerBot.bot.callback_query_handler(func=lambda call: call.data == 'parse')
def parser_controller(message):
    ControllerBot.bot.send_message(message.from_user.id,
                                 text='Что вам нужно?',
                                 reply_markup=KeyboardBuilder.make_parser_keyboard(ControllerBot.check_box))


@ControllerBot.bot.callback_query_handler(func=lambda call: call.data == 'change_account')
def change_account(message):
    msg = ControllerBot.bot.send_message(message.from_user.id, text='Введите id пользователя')






@ControllerBot.bot.callback_query_handler(func=lambda call: call.data == 'update_checkbox')
def update_checkbox(message):
    pass


@ControllerBot.bot.callback_query_handler(func=lambda call: call.data == 'update_sources')
def update_sources(message):
    pass


@ControllerBot.bot.callback_query_handler(func=lambda call: call.data == 'update_filters')
def update_filters(message):
    pass

@ControllerBot.bot.callback_query_handler(func=lambda call: call.data == 'update_stoplist')
def update_stoplist(message):
    pass

@ControllerBot.bot.callback_query_handler(func=lambda call: call.data == 'update_admin_msg')
def update_admin_msg(message):
    pass


ControllerBot.bot.polling(none_stop=True, interval=0)