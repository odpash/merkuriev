import datetime
import os
import types

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile
import logic
from keyboards import main_menu, ok, back
from db import create_new, count, update_approve, update_pay, update_postlink, update_text, delete_post
from logic import to_approve, to_pay, find, active

bot = Bot(token="5012003579:AAFZA9fTzzxL7WL1COMOmypCuExpMZOTHvg")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())
cat1, cat2, cat3 = [], [], []
m_id = []


class Form(StatesGroup):
    text_or_photo = State()


@dp.message_handler(state=Form.text_or_photo, content_types=['photo'])
async def abc(message, state):
    async with state.proxy() as data:
        u_id = data['a'].split()[0]
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f'database/{u_id}.jpg')
    os.remove(path)
    await message.photo[-1].download(f'database/{u_id}.jpg')
    await state.finish()
    await message.answer("Фото успешно изменено.")
    message.text = "/start"
    await start(message)


@dp.message_handler(state=Form.text_or_photo, content_types=['text'])
async def cba(message, state):
    async with state.proxy() as data:
        u_id = data['a'].split()[0]
        f = data['a'].split()[1]
    await state.finish()
    if ('f' in f) or ("Вернуться в меню" in message.text):
        message.text = '/start'
        await start(message)
        return
    await update_text(u_id, message.text)
    await message.answer("Описание успешно обновлено.")
    message.text = '/start'
    await start(message)

async def alert(c):
    for i in c:
        await bot.send_message(i, "Появилась новая информация!")


async def send_to_chanel(message, photo):
    chanel_name = -1001742419815
    await bot.send_photo(chanel_name, photo=photo, caption=message)


@dp.callback_query_handler(lambda c: 'find_' in c.data)
async def findcb(query):
    global m_id
    await bot.answer_callback_query(query.id)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    m_id = await logic.find_2(query.data.replace('find_', ''), bot, query.message)


@dp.callback_query_handler(lambda c: 'approve' in c.data or 'pay_' in c.data)
async def approve_cb_or_pay_cb(query):
    global m_id
    await bot.answer_callback_query(query.id)
    if ('_ok' not in query.data) and ('approve4' in query.data or 'approve1' in query.data or 'pay' in query.data):
        m_id.append(await bot.send_message(query.message.chat.id, "Нажмите `подтвердить` для выполнения действия",
                                           reply_markup=ok(query.data.split('_')[0], query.data.split('_')[1])))
        return

    query['from']['first_name'], query['from']['last_name'] = str(query['from']['first_name']), str(
        query['from']['last_name'])
    query.data = query.data.replace('_ok', '')
    if 'approve' in query.data:
        u_id = int(query.data.split('_')[1])
        cmd = query.data.split('_')[0]
        if cmd == 'approve1':
            await update_approve(u_id, query['from']['username'], query['from']['first_name'] + " " +
                                 query['from']['last_name'], query['from']['id'])
            await alert(cat2)
        elif cmd == 'approve2':
            state = Dispatcher.get_current().current_state()
            async with state.proxy() as data:
                data['a'] = str(u_id) + ' f'
            await bot.send_message(query.message.chat.id, "Отправьте новое фото", reply_markup=back())
            await Form.text_or_photo.set()
            return
        elif cmd == 'approve3':
            state = Dispatcher.get_current().current_state()
            async with state.proxy() as data:
                data['a'] = str(u_id) + ' t'
            await bot.send_message(query.message.chat.id, "Отправьте новое описание", reply_markup=back())
            await Form.text_or_photo.set()
            return
        elif cmd == 'approve4':
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f'database/{u_id}.jpg')
            os.remove(path)
            await delete_post(u_id)
    else:
        query.data = int(query.data.replace('pay_', ''))
        await update_pay(query.data, query['from']['username'], query['from']['first_name'] + " " +
                         query['from']['last_name'], query['from']['id'])
        await alert(cat3)
    await query.answer("Изменения успешно сохранены.")
    await bot.send_message(query.message.chat.id, "Изменения успешно сохранены!")
    if len(m_id) > 0:
        for i in m_id:
            await bot.delete_message(query.message.chat.id, i.message_id)
        m_id = []

@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    global m_id
    if message['from']['username'] == 'GroupAnonymousBot':
        return
    if message['from']['id'] == 777000 and "ID: " in str(message.caption):
        a = int(message.caption.split()[1].strip())
        l = f'https://t.me/c/1742419815/{message["forward_from_message_id"]}'
        print(a, l)
        await update_postlink(a, l)
        return
    elif message['from']['id'] != 777000:
        item_id = count() + 1
        await create_new(message.caption, item_id, message['from']['username'],
                         str(message['from']['first_name']) + " " +
                         str(message['from']['last_name']), message['from']['id'])
        await message.photo[-1].download(f'database/{item_id}.jpg')
        a = datetime.datetime.now()
        dop_a, dop_b, dop_c, dop_d = '', '', '', ''
        if len(str(a.hour)) == 1:
            dop_a = '0'
        if len(str(a.minute)) == 1:
            dop_b = '0'
        if len(str(a.day)) == 1:
            dop_c = '0'
        if len(str(a.month)) == 1:
            dop_d = '0'

        photo = InputFile(f"database/{item_id}.jpg")
        await send_to_chanel(
            f"ID: {item_id}\nТекст: " + str(message.caption).replace("None", "") + "\n" + dop_a + str(a.hour) + ":" + dop_b + str(
                a.minute) + ' ' + dop_c + str(a.day) + '.' + dop_d + str(a.month) + '.' + str(a.year), photo)
        await message.answer("Запись успешно сохранена!")
        await alert(cat1)


@dp.message_handler(content_types=['text'])
async def start(message):
    global m_id
    if message.chat.id == -1001742419815 or message['from']['username'] == 'GroupAnonymousBot':
        return
    if len(m_id) > 0:
        for i in m_id:
            await bot.delete_message(message.chat.id, i.message_id)
        m_id = []
    if message.text == '/start' or message.text == 'Вернуться в меню':
        await message.answer(
            f"Здравствуйте, {str(message['from']['first_name'])}!\nЧтобы включить (отключить) оповещения о появлении"
            f" новых счетов напишите /new\nДля включения (отключения) оповещений о согласовании "
            f"счета напишите /approve\nДля включения (отключения) оповещений об оплате напишите /pay",
            reply_markup=main_menu())
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
        await message.answer("Отправьте фото со счетом и напишите необходимую подпись (все в одном сообщении):\n(здесь показано место куда нужно нажать для добавления коментариев)")
        photo1 = open('add_desription.png', 'rb')
        photo2 = open('add_description_2.jpg', 'rb')
        await bot.send_media_group(chat_id=message.chat.id, media=[{'type': 'photo', 'media': photo1}, {'type': 'photo', 'media': photo2}])
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
        await message.answer("Введите текст поиска:")

    elif len(message.text) == 10 and message.text[2] == '.' and message.text[5] == '.':
        text = message.text
        text = text[6::] + '-' + text[3:5] + '-' + text[0:2]
        m_id = await logic.find_2(text, bot, message)
    else:
        await logic.find_2(message.text, bot, message)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=print("Бот запущен"))
