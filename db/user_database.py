import sqlite3


class MyDatabase:
    def __init__(self):
        print('evoked constructor ')
        self.db = sqlite3.connect('test_db')
        self.cursor = self.db.cursor()
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS stats(id INTEGER PRIMARY KEY, 
        money INTEGER, health INTEGER, inventory TEXT)''')
        self.db.commit()
        # information which saved instance of a game is currently played
        self.row_id = 1

    def insert(self):  # create new row with new game instance, and automatically set row_id
        print('evoked insert')
        self.cursor.execute('''INSERT INTO stats(money, health, inventory)
        VALUES(?, ?, ?)''', (0, 0, ""))
        self.db.commit()
        self.row_id = self.cursor.lastrowid
        return self.cursor.lastrowid

    def update_money(self, money):
        self.cursor.execute('''UPDATE stats SET money = ? WHERE id = ? ''', (money, self.row_id))
        self.db.commit()

    def get_money(self):
        self.cursor.execute('''SELECT money FROM stats WHERE id = ?''', (self.row_id, ))
        money = self.cursor.fetchone()
        return money[0]

    def get_version(self):
        return self.row_id


