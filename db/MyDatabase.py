import sqlite3
import os
from datetime import datetime
db_path = os.path.abspath('../data/stats_db')  # path to database


class MyDatabase:
    def __init__(self):
        print('evoked constructor ')
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS stats(id INTEGER PRIMARY KEY, 
        money INTEGER, health INTEGER, inventory TEXT, last_saved TIMESTAMP, if_new INTEGER)''')
        self.db.commit()
        self.cursor.execute("SELECT COUNT(*) FROM stats")
        rows = self.cursor.fetchone()
        rows_nr = rows[0]
        while rows_nr < 3:
            self.new_row()
            rows_nr += 1

    def new_row(self):  # create new row with new game instance, and automatically set row_id
        print('evoked insert')
        self.cursor.execute('''INSERT INTO stats(money, health, inventory, last_saved, if_new)
        VALUES(?, ?, ?, ?, ?)''', (0, 0, "", datetime.now(tz=None), 1))
        self.db.commit()
        return self.cursor.lastrowid

    def update_money(self, money, row_id):
        self.cursor.execute('''UPDATE stats SET money = ? WHERE id = ? ''', (money, row_id))
        self.db.commit()

    def update_date(self, row_id):
        self.cursor.execute('''UPDATE stats SET last_saved = ? WHERE id = ?''', (datetime.now(tz=None), row_id))
        self.db.commit()

    def update_if_new(self, row_id):
        self.cursor.execute('''UPDATE stats SET if_new = ? WHERE id = ?''', (0, row_id))
        self.db.commit()

    def get_money(self, row_id):
        self.cursor.execute('''SELECT money FROM stats WHERE id = ?''', (row_id, ))
        money = self.cursor.fetchone()
        return money[0]

    def get_date(self, row_id):
        self.cursor.execute('''SELECT last_saved FROM stats WHERE id = ?''', (row_id, ))
        date = self.cursor.fetchone()
        return date[0]

    def get_if_new(self, row_id):
        self.cursor.execute('''SELECT if_new FROM stats WHERE id = ?''', (row_id, ))
        if_new = self.cursor.fetchone()
        return if_new[0]

    def reset_db(self):
        self.cursor.execute('''DELETE FROM stats''')

    def reset_row(self, row_id):
        self.cursor.execute('''UPDATE stats SET money = ?, health = ?, inventory = ?, last_saved = ?, if_new = ?''',
                            (0, 0, "", datetime.now(), 1))


