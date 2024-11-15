from telebot import types


def create_choice_buttons():
    markup = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton('👍', callback_data='start')
    delete_button = types.InlineKeyboardButton('👎', callback_data='delete')
    markup.add(start_button, delete_button)
    return markup


def create_choice_price_buttons(id_auction, start_price):
    markup = types.InlineKeyboardMarkup(row_width=3)
    button_25 = types.InlineKeyboardButton(f'{round(start_price * 0.75)}',
                                           callback_data=f'{round(start_price * 0.75)} {id_auction}')
    button_50 = types.InlineKeyboardButton(f'{round(start_price * 0.5)}',
                                           callback_data=f'{round(start_price * 0.75)} {id_auction}')
    button_75 = types.InlineKeyboardButton(f'{round(start_price * 0.25)}',
                                           callback_data=f'{round(start_price * 0.75)} {id_auction}')
    button_100 = types.InlineKeyboardButton('0', callback_data=f'0 {id_auction}')
    back_button = types.InlineKeyboardButton('« Назад', callback_data=f'back {id_auction}')
    markup.add(button_25, button_50, button_75, button_100)
    markup.add(back_button)
    return markup
