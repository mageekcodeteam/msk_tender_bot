import time
import schedule
import threading

from threading import *
from items import *
from telebot import TeleBot
from datetime import datetime
from config import TOKEN, GROUP_ID
from scanner import scanner
from database.database import get_auction
from script_1 import work_function_1
from script_2 import work_function_2

bot = TeleBot(TOKEN)

database = {}


@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message):
    if message.chat.id == GROUP_ID:
        bot.send_message(message.chat.id, 'Привет, Генеральный директор!')


def mailing_new_auctions():
    auctions = scanner()
    if type(auctions) == list:
        print(datetime.now(), len(auctions))
    else:
        print(datetime.now(), auctions)
    if auctions != 'Error':
        for auction in auctions:
            bot.send_message(GROUP_ID, auction, parse_mode='html', disable_web_page_preview=True)


@bot.callback_query_handler(func=lambda call: True)
def manage_commands(call: types.CallbackQuery):
    if call.data == 'start':
        auction_info = call.message.text.split('\n\n')
        bot.edit_message_text(chat_id=GROUP_ID, message_id=call.message.message_id,
                              text=f'{auction_info[2]}\n\n'
                                   f'{auction_info[-1]}\n\n'
                                   f'<b>До какой цены опускаться?</b>',
                              reply_markup=create_choice_price_buttons(auction_info[-1].split('/')[-1],
                                                                       get_auction(
                                                                           int(auction_info[-1].split('/')[-1]))[2]),
                              parse_mode='html', disable_web_page_preview=True)
    elif call.data == 'delete':
        bot.delete_message(chat_id=GROUP_ID, message_id=call.message.message_id)
    elif call.data.split()[0] == 'back':
        auction_info = get_auction(int(call.data.split()[1]))
        bot.edit_message_text(chat_id=GROUP_ID, message_id=call.message.message_id,
                              text=f'Наименование: <b>{auction_info[0]}</b>\n\n'
                                   f'Организация: <b>{auction_info[1]}</b>\n\n'
                                   f'Начальная цена: <b>{auction_info[2]}</b>\n\n'
                                   f'Дата начала: <b>{auction_info[3]}</b>\n\n'
                                   f'Дата окончания: <b>{auction_info[4]}</b>\n\n'
                                   f'ФЗ: <b>{auction_info[5]}</b>\n\n'
                                   f'Ссылка: https://zakupki.mos.ru/auction/{auction_info[-1]}',
                              reply_markup=create_choice_buttons(), parse_mode='html', disable_web_page_preview=True)
    elif call.data.split()[0].isdigit():
        database['url_auction'] = f'https://zakupki.mos.ru/auction/{call.data.split()[1]}'
        database['min_price'] = call.data.split()[0]
        bot.send_message(GROUP_ID, f'Отправьте authorization ИП Аванесов\n\n'
                                   f'https://zakupki.mos.ru/auction/{call.data.split()[1]}')


# @bot.message_handler(content_types=['text'])
# def manage_authorization(message):
#     global database
#     if message.text.startswith('Bearer'):
#         if 'authorization_1' not in database:
#             database['authorization_1'] = message.text
#             bot.send_message(GROUP_ID, f'Отправьте authorization ИП Свеженцов\n\n'
#                                        f'{database["url_auction"]}')
#         else:
#             database['authorization_2'] = message.text
#             t1 = threading.Thread(target=work_function_1,
#                                   args=(database['authorization_1'], database['url_auction'], database['min_price']))
#             t2 = threading.Thread(target=work_function_1,
#                                   args=(database['authorization_1'], database['url_auction'], database['min_price']))
#             t3 = threading.Thread(target=work_function_1,
#                                   args=(database['authorization_1'], database['url_auction'], database['min_price']))
#             t4 = threading.Thread(target=work_function_1,
#                                   args=(database['authorization_1'], database['url_auction'], database['min_price']))
#             t5 = threading.Thread(target=work_function_2,
#                                   args=(database['authorization_2'], database['url_auction'], database['min_price']))
#             t6 = threading.Thread(target=work_function_2,
#                                   args=(database['authorization_2'], database['url_auction'], database['min_price']))
#             t7 = threading.Thread(target=work_function_2,
#                                   args=(database['authorization_2'], database['url_auction'], database['min_price']))
#             t8 = threading.Thread(target=work_function_2,
#                                   args=(database['authorization_2'], database['url_auction'], database['min_price']))
#             t1.start()
#             t2.start()
#             t3.start()
#             t4.start()
#             t5.start()
#             t6.start()
#             t7.start()
#             t8.start()
#             database = {}


def timer():
    print('Scanner online')
    while True:
        schedule.run_pending()
        time.sleep(1)


def start_timer():
    schedule.every(2).minutes.do(mailing_new_auctions)
    t1 = Thread(target=timer)
    t1.start()


if __name__ == '__main__':
    print('Bot online')
    start_timer()
    bot.polling(none_stop=True)
