from aiogram import Bot, Dispatcher, executor

from keyboards import main_menu
from db import create_new, count, update_approve, update_pay
from logic import to_approve, to_pay, all, active

bot = Bot(token="2111238966:AAEQrHDXicLlfPw99uqU2QFMBoexIsZTxzk")
dp = Dispatcher(bot)
cat1, cat2, cat3 = [], [], []


async def alert(c):
    for i in c:
        await bot.send_message(i, "Появилась новая информация!")


@dp.callback_query_handler(lambda c: 'approve_' in c.data or 'pay_' in c.data)
async def approve_cb_or_pay_cb(query):
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
    item_id = count() + 1
    await create_new(message.caption, item_id, message['from']['username'], message['from']['first_name'] + " " +
                     message['from']['last_name'], message['from']['id'])
    await message.photo[-1].download(f'database/{item_id}.jpg')
    await message.answer("Запись успешно сохранена!")
    await alert(cat1)


@dp.message_handler(content_types=['text'])
async def start(message):
    if message.text == '/start':
        await message.answer(
            f"Здравствуйте, {message['from']['first_name']}!\nЧтобы включить (отключить) оповещения о появлении"
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
        await to_approve(message, bot)
    elif message.text == "К оплате":
        await message.answer("Счета к оплате")
        await to_pay(message, bot)
    elif message.text == "Активные счета":
        await message.answer("Активные счета")
        await active(message, bot)
    elif message.text == "Все счета":
        await message.answer("Все счета: ")
        await all(message, bot)
    else:
        await message.answer("Такой команды не существует...", reply_markup=main_menu())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=print("Бот запущен"))
