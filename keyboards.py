from aiogram import types


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.InlineKeyboardButton("Создать счет"))
    markup.row(types.InlineKeyboardButton("К согласованию"), types.InlineKeyboardButton("К оплате"))
    markup.row(types.InlineKeyboardButton("Активные счета"), types.InlineKeyboardButton("Все счета"))
    return markup


def approve_btn(id):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("Согласовать", callback_data=f"approve_{id}"))
    return markup


def pay_btn(id):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("Оплатить", callback_data=f"pay_{id}"))
    return markup