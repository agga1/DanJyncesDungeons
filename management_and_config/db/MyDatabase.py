import sqlite3
import os
from datetime import datetime

from management_and_config.configurations import start_health, start_lvl

db_path = os.path.abspath('../data/stats_db')  # path to database
# TODO add column, getters and updaters (S: dropped items (?), curr_world, curr_room, items in inv, skills,
#  opened/closed doors)


class MyDatabase:
    def __init__(self):
        print('evoked constructor ')
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS stats(id INTEGER PRIMARY KEY, 
        money INTEGER, health INTEGER, experience INTEGER, lvl INTEGER, active_enemies TEXT, 
        inventory TEXT, last_saved TIMESTAMP, if_new INTEGER)''')
        self.db.commit()
        self.cursor.execute("SELECT COUNT(*) FROM stats")
        rows = self.cursor.fetchone()
        rows_nr = rows[0]
        while rows_nr < 3:
            self.new_row()
            rows_nr += 1

        self.row_id = 1

    def set_row_id(self, row_id):
        self.row_id = row_id

    def new_row(self):  # create new row with new game instance, and automatically set row_id
        print('evoked insert')
        self.cursor.execute('''INSERT INTO stats(money, health, experience, lvl, active_enemies, inventory, last_saved, if_new)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)''', (0, start_health, 0, start_lvl, "", "", datetime.now(tz=None), 1))
        self.db.commit()
        return self.cursor.lastrowid

    def update_active_enemies(self, act_en, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        self.cursor.execute('''UPDATE stats SET active_enemies = ? WHERE id = ? ''', (act_en, row_id))
        self.db.commit()

    def update_date(self, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        self.cursor.execute('''UPDATE stats SET last_saved = ? WHERE id = ?''', (datetime.now(tz=None), row_id))
        self.db.commit()

    def update_experience(self, exp, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        self.cursor.execute('''UPDATE stats SET experience = ? WHERE id = ? ''', (exp, row_id))
        self.db.commit()

    def update_health(self, health, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        self.cursor.execute('''UPDATE stats SET health = ? WHERE id = ? ''', (health, row_id))
        self.db.commit()

    def update_if_new(self, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        self.cursor.execute('''UPDATE stats SET if_new = ? WHERE id = ?''', (0, row_id))
        self.db.commit()

    def update_lvl(self, lvl, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        self.cursor.execute('''UPDATE stats SET lvl = ? WHERE id = ? ''', (lvl, row_id))
        self.db.commit()

    def update_money(self, money, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        self.cursor.execute('''UPDATE stats SET money = ? WHERE id = ? ''', (money, row_id))
        self.db.commit()

    def get_active_enemies(self, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        self.cursor.execute('''SELECT active_enemies FROM stats WHERE id = ?''', (row_id, ))
        act_en = self.cursor.fetchone()
        return act_en[0]

    def get_money(self, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        self.cursor.execute('''SELECT money FROM stats WHERE id = ?''', (row_id, ))
        money = self.cursor.fetchone()
        return money[0]

    def get_health(self, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        self.cursor.execute('''SELECT health FROM stats WHERE id = ?''', (row_id,))
        health = self.cursor.fetchone()
        return health[0]

    def get_experience(self, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        self.cursor.execute('''SELECT experience FROM stats WHERE id = ?''', (row_id, ))
        exp = self.cursor.fetchone()
        return exp[0]

    def get_lvl(self, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        self.cursor.execute('''SELECT lvl FROM stats WHERE id = ?''', (row_id, ))
        lvl = self.cursor.fetchone()
        return lvl[0]

    def get_date(self, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        self.cursor.execute('''SELECT last_saved FROM stats WHERE id = ?''', (row_id, ))
        date = self.cursor.fetchone()
        return date[0]

    def get_if_new(self, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        self.cursor.execute('''SELECT if_new FROM stats WHERE id = ?''', (row_id, ))
        if_new = self.cursor.fetchone()
        return if_new[0]

    def reset_db(self):
        self.cursor.execute('''DELETE FROM stats''')

    def reset_row(self, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        self.cursor.execute('''UPDATE stats SET money = ?, health = ?, experience = ?, lvl = ?, active_enemies = ?, inventory = ?, last_saved = ?, if_new = ? WHERE id = ?''',
                            (0, start_health, 0, start_lvl, "", "", datetime.now(), 1, row_id))
        self.db.commit()

