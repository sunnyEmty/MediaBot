import telebot
from make_keyboards import KeyboardBuilder
from config import TOKEN

controller_bot = telebot.TeleBot(token=TOKEN)


@controller_bot.message_handler(content_types=['text', 'document', 'audio'])
def get_start_msg(message):
    if message.text != '/run':
        controller_bot.send_message(message.from_user.id, 'Привет! Введи /run для начала работы :)')
    else:
        controller_bot.send_message(message.from_user.id,
                                    text='Выбери нужного бота.',
                                    reply_markup=KeyboardBuilder.make_bots_keyboard())


@controller_bot.callback_query_handler(func=lambda call: call.data == 'parser_controller')
def parser_controller(message):
    controller_bot.send_message(message.from_user.id,
                                text='Привет, я Парсер! Какие указания?',
                                reply_markup=KeyboardBuilder.make_parser_keyboard())



def poster_controller():
    pass


def sender_controller():
    pass


controller_bot.polling(none_stop=True, interval=0)