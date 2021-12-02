from aiogram.types import InputFile
from db import all_info
from keyboards import approve_btn, pay_btn


async def to_approve(message, bot):
    dbase = all_info()
    for i in dbase:
        if i[9] is None:
            text = f"Id: {i[0]},\nТекст: {i[1]},\n\nИнформация о создании файла:\nUsername создателя: {i[2]}," \
                    f"\nФамилия и имя: {i[3]},\nTelegramId: {i[4]}\nДата создания: {i[5]}"
            photo = InputFile(f"database/{i[0]}.jpg")
            await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=text, reply_markup=approve_btn(i[0]))


async def to_pay(message, bot):
    dbase = all_info()
    for i in dbase:
        if i[13] is None and i[9] is not None:
            text = f"Id: {i[0]},\nТекст: {i[1]},\n\nИнформация о создании файла:\nUsername создателя: {i[2]}," \
                   f"\nФамилия и имя: {i[3]},\nTelegramId: {i[4]}\nДата создания: {i[5]}\n\nИнформация о " \
                   f"согласовании файла:\nUsername согласующего: {i[6]},\nФамилия и имя: {i[7]},\nTelegramId: {i[8]}" \
                   f"\nДата согласования: {i[9]}"
            photo = InputFile(f"database/{i[0]}.jpg")
            await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=text, reply_markup=pay_btn(i[0]))


async def active(message, bot):
    await to_approve(message, bot)
    await to_pay(message, bot)


async def all(message, bot):
    dbase = all_info()
    for i in dbase:
        text = f"Id: {i[0]},\nТекст: {i[1]},\n\nИнформация о создании файла:\nUsername создателя: {i[2]}," \
            f"\nФамилия и имя: {i[3]},\nTelegramId: {i[4]}\nДата создания: {i[5]}\n\nИнформация о " \
            f"согласовании файла:\nUsername согласующего: {i[6]},\nФамилия и имя: {i[7]},\nTelegramId: {i[8]}" \
            f"\nДата согласования: {i[9]}\n\nИнформация об оплате:\nUsername оплатившего: {i[10]}," \
               f"\nФамилия и имя: {i[11]},\nTelegramId: {i[12]},\nДата оплаты: {i[13]}".replace('None', '-')
        photo = InputFile(f"database/{i[0]}.jpg")
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=text)
