import datetime
import sqlite3
import datetime


async def create_new(text, item_id, creator_username, creator_real_name, creator_telegram_id):
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    created_time = datetime.datetime.now()
    cursor = sqlite_connection.cursor()
    sqlite_insert_query = f"""INSERT INTO items (id, itemText, creatorUsername, creatorRealName, creatorTelegramId, createdTime, postlink)
      VALUES  ({item_id}, '{text}', '{creator_username}', '{creator_real_name}', '{creator_telegram_id}', '{created_time}', '')"""
    cursor.execute(sqlite_insert_query)
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
