import sqlite3
import os
from datetime import datetime

from management_and_config.configurations import start_health, start_lvl

db_path = os.path.abspath('../data/stats_db')  # path to database
# TODO curr_room, curr_world
# TODO add column, getters and updaters (S: dropped items (?), items in inv, skills opened/closed doors)
columns = ["id", "INTEGER PRIMARY KEY",
           "money", "INTEGER",
           "health", "INTEGER",
           "experience", "INTEGER",
           "lvl", "INTEGER",
           "active_enemies", "TEXT",
           "inventory", "TEXT",
           "curr_room", "TEXT",
           "curr_world", "INTEGER",
           "last_saved", "TIMESTAMP",
           "if_new", "INTEGER"]
values = (0, start_health, 0, start_lvl, "", "", None, None, datetime.now(tz=None), 1)

table_name = "stats"
# create_table command
create_table = ''' CREATE TABLE IF NOT EXISTS ''' + table_name + "("
for i in range(0, len(columns), 2):
    create_table += columns[i] + " " + columns[i + 1] + ", "
create_table = create_table[:-2]  # trim comma
create_table += ")"

# insert command
insert_into = '''INSERT INTO ''' + table_name + "("
for i in range(2, len(columns), 2):  # skip id!
    insert_into += columns[i] + ", "
insert_into = insert_into[:-2]  # trim last comma
insert_into += ") "
insert_into += "VALUES("
for i in range(2, len(columns), 2):
    insert_into += "?, "
insert_into = insert_into[:-2]
insert_into += ")"

# reset row
reset_row = '''UPDATE ''' + table_name + " SET "
for i in range(2, len(columns), 2):
    reset_row += columns[i] + " = ?, "
reset_row = reset_row[:-2]
reset_row += ''' WHERE id = '''


class MyDatabase:
    def __init__(self):
        print('evoked constructor ')
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
        self.cursor.execute(create_table)
        print(reset_row)
        self.db.commit()
        self.cursor.execute("SELECT COUNT(*) FROM " + table_name)
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
        self.cursor.execute(insert_into, values)
        self.db.commit()
        return self.cursor.lastrowid

    def update_column(self, col_name, value, row_id):
        cmd_str = "UPDATE " + table_name + " SET " + col_name + " = ? WHERE id = ? "
        self.cursor.execute(cmd_str, (value, row_id))

    def update_active_enemies(self, act_en, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        self.cursor.execute('''UPDATE stats SET active_enemies = ? WHERE id = ? ''', (act_en, row_id))
        self.db.commit()

    def update_curr_room(self, room, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        self.cursor.execute('''UPDATE stats SET curr_room = ? WHERE id = ? ''', (room, row_id))
        self.db.commit()

    def update_curr_world(self, world, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        self.cursor.execute('''UPDATE stats SET curr_world = ? WHERE id = ? ''', (world, row_id))
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

    def get_curr_room(self, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        self.cursor.execute('''SELECT curr_room FROM stats WHERE id = ?''', (row_id, ))
        room = self.cursor.fetchone()
        return room[0]

    def get_curr_world(self, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        self.cursor.execute('''SELECT curr_world FROM stats WHERE id = ?''', (row_id, ))
        world = self.cursor.fetchone()
        return world[0]

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
        self.cursor.execute('''DELETE FROM ''' + table_name)

    def reset_row(self, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        self.cursor.execute(reset_row + str(row_id),
                            values)
        self.db.commit()


# insert command
"""'''INSERT INTO stats(money, health, experience, lvl, active_enemies, inventory, curr_room, 
        curr_world, last_saved, if_new) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''"""
# reset row
"""'''UPDATE stats SET money = ?, health = ?, experience = ?, lvl = ?, active_enemies = ?, 
        inventory = ?, curr_room = ?, curr_world = ?, last_saved = ?, if_new = ? WHERE id = ''' + str(self.row_id)"""
