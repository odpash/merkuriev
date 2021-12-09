from aiogram import types
from aiogram.types import InputFile

import keyboards
from db import all_info
from keyboards import approve_btn, pay_btn


async def to_approve(message, bot):
    dbase = all_info()
    m_id = []
    for i in dbase:
        if i[9] is None:
            t = i[5].split()[0]
            t_norm = t[8::] + '.' + t[5:7] + '.' + t[0:4]
            text = f"{i[1]},\nДата: {t_norm}\nОбсуждение: {i[14]}"
            photo = InputFile(f"database/{i[0]}.jpg")
            m_id.append(await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=text, reply_markup=approve_btn(i[0])))
    return m_id

async def to_pay(message, bot):
    m_id = []
    dbase = all_info()
    for i in dbase:
        if i[13] is None and i[9] is not None:
            t = i[5].split()[0]
            t_norm = t[8::] + '.' + t[5:7] + '.' + t[0:4]
            text = f"{i[1]},\nДата: {t_norm}\nCогласовал: {i[7]} ({i[6]})\nОбсуждение: {i[14]}"
            photo = InputFile(f"database/{i[0]}.jpg")
            m_id.append(await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=text, reply_markup=pay_btn(i[0])))
    return m_id


async def active(message, bot):
    m_id = await to_approve(message, bot)
    m_id_2 = await to_pay(message, bot)
    for i in m_id_2:
        m_id.append(i)
    return m_id

async def find(message, bot):
    dbase = all_info()
    dates = []
    dates_norm = []
    markup = types.InlineKeyboardMarkup()
    for i in dbase:
        t = i[5].split()[0]
        if t not in dates:
            dates.append(t)
            t_norm = t[8::] + '.' + t[5:7] + '.' + t[0:4]
            dates_norm.append(t_norm)
    for i in range(0, len(dates_norm), 3):
        if i == len(dates_norm) - 1:
            markup.row(types.InlineKeyboardButton(dates_norm[i], callback_data=f"find_{dates[i]}"))
        elif i == len(dates_norm) - 2:
            markup.row(types.InlineKeyboardButton(dates_norm[i], callback_data=f"find_{dates[i]}"),
                       types.InlineKeyboardButton(dates_norm[i + 1], callback_data=f"find_{dates[i + 1]}"))
        else:
            markup.row(types.InlineKeyboardButton(dates_norm[i], callback_data=f"find_{dates[i]}"),
                       types.InlineKeyboardButton(dates_norm[i + 1], callback_data=f"find_{dates[i + 1]}"),
                       types.InlineKeyboardButton(dates_norm[i + 2], callback_data=f"find_{dates[i + 2]}"))

    await message.answer("Выберите дату или введите в формате (dd.mm.yyyy):", reply_markup=markup)



async def find_2(text_a, bot, message):
    dbase = all_info()
    m_id = []
    fl = False
    for i in dbase:
        if text_a in i[5]:
            fl = True
            text = f"Выбранная дата: {i[5]}\nId: {i[0]},\nТекст: {i[1]},\n\nИнформация о создании файла:\nUsername создателя: {i[2]}," \
                   f"\nФамилия и имя: {i[3]},\nTelegramId: {i[4]}\nДата создания: {i[5]}\n\nИнформация о " \
                   f"согласовании файла:\nUsername согласующего: {i[6]},\nФамилия и имя: {i[7]},\nTelegramId: {i[8]}" \
                   f"\nДата согласования: {i[9]}\n\nИнформация об оплате:\nUsername оплатившего: {i[10]}," \
                   f"\nФамилия и имя: {i[11]},\nTelegramId: {i[12]},\nДата оплаты: {i[13]}".replace('None', '-')
            photo = InputFile(f"database/{i[0]}.jpg")
            m_id.append(await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=text, reply_markup=keyboards.back()))
    if not fl:
        m_id.append(await bot.send_message(message.chat.id, "Ничего не найдено :("))
    return m_id