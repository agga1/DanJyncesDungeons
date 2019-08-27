import sqlite3

db = sqlite3.connect('data/test_db')
CREATE_TABLE = '''
    CREATE TABLE stats(id INTEGER AUTOINCREMENT PRIMARY KEY, money INTEGER, health INTEGER, inventory TEXT)
'''
cursor = db.cursor()
cursor.execute(CREATE_TABLE)
db.commit()


def insert(): # create new row with new game instance
    cursor.execute('''INSERT INTO stats(money, health, inventory)
    VALUES(?, ?, ?)''', (0, 0, ""))
    db.commit()
    return cursor.lastrowid


def update_money(row_id, money):
    cursor.execute('''UPDATE stats SET money = ? WHERE id = ? ''', (money, row_id))
    db.commit()



