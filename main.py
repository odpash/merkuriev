import datetime

from aiogram import Bot, Dispatcher, executor
from aiogram.types import InputFile

import logic
from keyboards import main_menu
from db import create_new, count, update_approve, update_pay, update_postlink
from logic import to_approve, to_pay, find, active

bot = Bot(token="2111238966:AAEQrHDXicLlfPw99uqU2QFMBoexIsZTxzk")
dp = Dispatcher(bot)
cat1, cat2, cat3 = [], [], []
m_id = []

async def alert(c):
    for i in c:
        await bot.send_message(i, "Появилась новая информация!")

async def send_to_chanel(message, photo):
    chanel_name = "@olegpashtestchat"
    await bot.send_photo(chanel_name, photo=photo, caption=message)

@dp.callback_query_handler(lambda c: 'find_' in c.data)
async def findcb(query):
    global m_id
    await bot.answer_callback_query(query.id)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    m_id = await logic.find_2(query.data.replace('find_', ''), bot, query.message)

@dp.callback_query_handler(lambda c: 'approve_' in c.data or 'pay_' in c.data)
async def approve_cb_or_pay_cb(query):
    global m_id
    await bot.answer_callback_query(query.id)
    if len(m_id) > 0:
        for i in m_id:
            await bot.delete_message(query.message.chat.id, i.message_id)
        m_id = []
    query['from']['first_name'], query['from']['last_name'] = str(query['from']['first_name']), str(query['from']['last_name'])
    if 'approve' in query.data:
        query.data = int(query.data.replace('approve_', ''))
        await update_approve(query.data, query['from']['username'], query['from']['first_name'] + " " +
                             query['from']['last_name'], query['from']['id'])
        await alert(cat2)
    else:
        query.data = int(query.data.replace('pay_', ''))
        await update_pay(query.data, query['from']['username'], query['from']['first_name'] + " " +
                         query['from']['last_name'], query['from']['id'])
        await alert(cat3)
    await query.answer("Изменения успешно сохранены.")
    await bot.send_message(query.message.chat.id, "Изменения успешно сохранены!")



@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    if message['from']['id'] == 777000:
        a = int(message.caption.split()[1].replace(',', '').strip())
        l = f'https://t.me/{message["sender_chat"]["username"]}/{message["forward_from_message_id"]}'
        await update_postlink(a, l)
        return
    item_id = count() + 1
    await create_new(message.caption, item_id, message['from']['username'], str(message['from']['first_name']) + " " +
                     str(message['from']['last_name']), message['from']['id'])
    await message.photo[-1].download(f'database/{item_id}.jpg')
    a = datetime.datetime.now()
    photo = InputFile(f"database/{item_id}.jpg")
    await send_to_chanel(f"ID: {item_id}, " + str(message.text).replace("None", "") + "\n" + str(a.hour) + ":" + str(a.minute) + ' ' + str(a.day) + '.' + str(a.month) + '.' + str(a.year), photo)
    await message.answer("Запись успешно сохранена!")
    await alert(cat1)




@dp.message_handler(content_types=['text'])
async def start(message):
    if 'Обсуждение:' in message.text:
        pass
    global m_id
    if len(m_id) > 0:
        for i in m_id:
            await bot.delete_message(message.chat.id, i.message_id)
        m_id = []
    if message.text == '/start' or message.text == 'Вернуться в меню':
        await message.answer(
            f"Здравствуйте, {str(message['from']['first_name'])}!\nЧтобы включить (отключить) оповещения о появлении"
            f" новых счетов напишите /new\nДля включения (отключения) оповещений о согласовании "
            f"счета напишите /approve\nДля включения (отключения) оповещений об оплате напишите /pay", reply_markup=main_menu())
    elif message.text == '/new':
        if message.chat.id not in cat1:
            await message.answer("Оповещения о появлении новых счетов - вкл.")
            cat1.append(message.chat.id)
        else:
            await message.answer("Оповещения о появлении новых счетов - выкл.")
            cat1.remove(message.chat.id)
    elif message.text == '/approve':
        if message.chat.id not in cat2:
            await message.answer("Оповещения о согласовании счетов - вкл.")
            cat2.append(message.chat.id)
        else:
            await message.answer("Оповещения о согласовании счетов - выкл.")
            cat2.remove(message.chat.id)
    elif message.text == '/pay':
        if message.chat.id not in cat3:
            await message.answer("Оповещения об оплате счетов - вкл.")
            cat3.append(message.chat.id)
        else:
            await message.answer("Оповещения об оплате счетов - выкл.")
            cat3.remove(message.chat.id)
    elif message.text == "Создать счет":
        await message.answer("Отправьте фото со счетом и напишите необходимую подпись (все в одном сообщении):")
    elif message.text == "К согласованию":
        await message.answer("Cчета к согласованию:")
        m_id = await to_approve(message, bot)
    elif message.text == "К оплате":
        await message.answer("Счета к оплате")
        m_id = await to_pay(message, bot)
    elif message.text == "Активные счета":
        await message.answer("Активные счета")
        m_id = await active(message, bot)
    elif message.text == "Поиск счета":
        await find(message, bot)
    elif len(message.text) == 10 and message.text[2] == '.' and message.text[5] == '.':
        text = message.text
        text = text[6::] + '-' + text[3:5] + '-' + text[0:2]
        m_id = await logic.find_2(text, bot, message)
    else:
        await message.answer("Такой команды не существует...", reply_markup=main_menu())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=print("Бот запущен"))
