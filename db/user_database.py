import sqlite3


class MyDatabase:
    def __init__(self):
        print('evoked constructor ')
        self.db = sqlite3.connect('test_db')
        self.cursor = self.db.cursor()
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS stats(id INTEGER PRIMARY KEY, 
        money INTEGER, health INTEGER, inventory TEXT)''')
        self.db.commit()

    def insert(self): # create new row with new game instance
        print('evoked insert')
        self.cursor.execute('''INSERT INTO stats(money, health, inventory)
        VALUES(?, ?, ?)''', (0, 0, ""))
        self.db.commit()
        return self.cursor.lastrowid

    def update_money(self, row_id, money):
        self.cursor.execute('''UPDATE stats SET money = ? WHERE id = ? ''', (money, row_id))
        self.db.commit()



