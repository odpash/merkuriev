import datetime
import sqlite3
import datetime


async def create_new(text, item_id, creator_username, creator_real_name, creator_telegram_id, message_id):
    sqlite_connection = sqlite3.connect('sqlite_python.db')
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
    cursor = sqlite_connection.cursor()
    sqlite_insert_query = f"""INSERT INTO items (id, itemText, creatorUsername, creatorRealName, creatorTelegramId, createdTime, postlink, message_id)
      VALUES  ({item_id}, '{text}', '{creator_username}', '{creator_real_name}', '{creator_telegram_id}', '{dop_a + str(a.hour) + ":" + dop_b + str(a.minute) + ' ' + dop_c + str(a.day) + '.' + dop_d + str(a.month) + '.' + str(a.year)}', '', '{message_id}')"""
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()


async def update_text(id, text):
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    cursor = sqlite_connection.cursor()
    sql_update_query = f"Update items set itemText = '{text}' where id = {id}"
    cursor.execute(sql_update_query)
    sqlite_connection.commit()
    cursor.close()


async def delete_post(id):
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    cursor = sqlite_connection.cursor()
    sql_update_query = f"Delete from items where id = {id}"
    cursor.execute(sql_update_query)
    sqlite_connection.commit()
    cursor.close()



async def update_approve(id, approver_username, approver_real_name, approver_telegram_id):
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    cursor = sqlite_connection.cursor()
    approved_time = datetime.datetime.now()
    sql_update_query = f"""Update items set approverUsername = '{approver_username}', 
    approverRealName = '{approver_real_name}', approverTelegramId = '{approver_telegram_id}', approvedTime = '{approved_time}' where id = {id}"""
    cursor.execute(sql_update_query)
    sqlite_connection.commit()
    cursor.close()


async def update_postlink(id, postlink):
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    cursor = sqlite_connection.cursor()
    pay_time = datetime.datetime.now()
    sql_update_query = f"""Update items set postlink = '{postlink}' where id = {id}"""
    cursor.execute(sql_update_query)
    sqlite_connection.commit()
    cursor.close()

async def update_pay(id, pay_username, pay_real_name, pay_telegram_id):
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    cursor = sqlite_connection.cursor()
    pay_time = datetime.datetime.now()
    sql_update_query = f"""Update items set paidUsername = '{pay_username}', 
    paidRealName = '{pay_real_name}', paidTelegramId = '{pay_telegram_id}', paidTime = '{pay_time}' where id = {id}"""
    cursor.execute(sql_update_query)
    sqlite_connection.commit()
    cursor.close()


def count():
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    cursor = sqlite_connection.cursor()
    cursor.execute("select count(*) from items")
    fixture_count, = cursor.fetchone()
    cursor.close()
    return fixture_count


def all_info():
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    cursor = sqlite_connection.cursor()
    cursor.execute("""select * from items""")
    res = cursor.fetchall()
    cursor.close()
    return res


def get_message_id(u_id):
    a = all_info()
    for i in a:
        if str(i[0]) == str(u_id):
            return int(i[15])


def get_message_text(u_id):
    a = all_info()
    for i in a:
        if str(i[0]) == str(u_id):
            return str(i[1])