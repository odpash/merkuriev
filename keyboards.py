from aiogram import types


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.InlineKeyboardButton("Создать счет"))
    markup.row(types.InlineKeyboardButton("К согласованию"), types.InlineKeyboardButton("К оплате"))
    markup.row(types.InlineKeyboardButton("Активные счета"), types.InlineKeyboardButton("Поиск счета"))
    return markup


def approve_btn(id):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("Согласовать", callback_data=f"approve1_{id}"),
               types.InlineKeyboardButton("Удалить", callback_data=f"approve4_{id}"))
    markup.row(types.InlineKeyboardButton("Изменить фото / pdf", callback_data=f"approve2_{id}"),
               types.InlineKeyboardButton("Изменить текст", callback_data=f"approve3_{id}"))
    return markup


def pay_btn(id):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("Оплатить", callback_data=f"pay_{id}"))
    return markup


def ok(action, id):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("Подтвердить", callback_data=f"{action}_{id}_ok"))
    return markup


def back():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.InlineKeyboardButton("Вернуться в меню"))
    return markup


