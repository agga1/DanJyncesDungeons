import sqlite3
import os
from datetime import datetime

from management_and_config.configurations import start_health, start_lvl, character_start_attack_damage, \
    character_start_attack_speed, character_start_critical_attack_chance

db_path = os.path.abspath('../data/stats_db')  # path to database
# TODO add column, getters and updaters (S: dropped items (?), items in inv, skills opened/closed doors)
columns = ["id", "INTEGER PRIMARY KEY",
           # character stats
           "money", "INTEGER",
           "health", "INTEGER",
           "mana", "INTEGER",
           "experience", "INTEGER",
           "lvl", "INTEGER",
           "skill_points", "INTEGER",
           "attack_damage", "INTEGER",
           "attack_speed", "REAL",
           "critical_attack_chance", "REAL",
           # room&world state
           "active_enemies", "TEXT",
           "inventory", "TEXT",
           "curr_room", "TEXT",
           "curr_world", "INTEGER",
           # general game state
           "last_saved", "TIMESTAMP",
           "if_new", "INTEGER"]
start_values = {"money": 0,
                "health": start_health,
                "mana": 0,
                "experience": 0,
                "lvl": start_lvl,
                "skill_points": 0,
                "attack_damage": character_start_attack_damage,
                "attack_speed": character_start_attack_speed,
                "critical_attack_chance": character_start_critical_attack_chance,
                "active_enemies": "",
                "inventory": "",
                "curr_room": None,   # needs to be updated in world during first startup
                "curr_world": None,  # same (or should be 1?)
                "last_saved": datetime.now(tz=None),
                "if_new": 1}
values = []
for i in range(2, len(columns), 2):
    values.append(start_values[columns[i]])
values = tuple(values)

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
        print(values)
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

    def update_column(self, col_name, value, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        cmd_str = "UPDATE " + table_name + " SET " + col_name + " = ? WHERE id = ? "
        self.cursor.execute(cmd_str, (value, row_id))
        self.db.commit()

    def get_column(self, col_name, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        cmd_str = "SELECT " + col_name + " FROM " + table_name + " WHERE id = ? "
        self.cursor.execute(cmd_str, (row_id, ))
        result = self.cursor.fetchone()
        return result[0]

    def update_active_enemies(self, value, row_id=-1):
        self.update_column("active_enemies", value, row_id)

    def update_mana(self, value, row_id=-1):
        self.update_column("mana", value, row_id)

    def update_skill_points(self, value, row_id=-1):
        self.update_column("skill_points", value, row_id)

    def update_attack_damage(self, value, row_id=-1):
        self.update_column("attack_damage", value, row_id)

    def update_attack_speed(self, value, row_id=-1):
        self.update_column("attack_speed", value, row_id)

    def update_critical_attack_chance(self, value, row_id=-1):
        self.update_column("critical_attack_chance", value, row_id)

    def update_curr_room(self, value, row_id=-1):
        self.update_column("curr_room", value, row_id)

    def update_curr_world(self, value, row_id=-1):
        self.update_column("curr_world", value, row_id)

    def update_date(self, row_id=-1):
        self.update_column("last_saved", datetime.now(tz=None), row_id)

    def update_experience(self, value, row_id=-1):
        self.update_column("experience", value, row_id)

    def update_health(self, value, row_id=-1):
        self.update_column("health", value, row_id)

    def update_if_new(self, row_id=-1):
        self.update_column("if_new", 0, row_id)

    def update_lvl(self, value, row_id=-1):
        self.update_column("lvl", value, row_id)

    def update_money(self, value, row_id=-1):
        self.update_column("money", value, row_id)

    def get_active_enemies(self, row_id=-1):
        return self.get_column("active_enemies", row_id)

    def get_mana(self, row_id=-1):
        return self.get_column("mana", row_id)

    def get_skill_points(self, row_id=-1):
        return self.get_column("skill_points", row_id)

    def get_attack_damage(self, row_id=-1):
        return self.get_column("attack_damage", row_id)

    def get_attack_speed(self, row_id=-1):
        return self.get_column("attack_speed", row_id)

    def get_critical_attack_chance(self, row_id=-1):
        return self.get_column("critical_attack_chance", row_id)

    def get_curr_room(self, row_id=-1):
        return self.get_column("curr_room", row_id)

    def get_curr_world(self, row_id=-1):
        return self.get_column("curr_world", row_id)

    def get_money(self, row_id=-1):
        return self.get_column("money", row_id)

    def get_health(self, row_id=-1):
        return self.get_column("health", row_id)

    def get_experience(self, row_id=-1):
        return self.get_column("experience", row_id)

    def get_lvl(self, row_id=-1):
        return self.get_column("lvl", row_id)

    def get_date(self, row_id=-1):
        return self.get_column("last_saved", row_id)

    def get_if_new(self, row_id=-1):
        return self.get_column("if_new", row_id)

    def reset_db(self):
        self.cursor.execute('''DELETE FROM ''' + table_name)

    def reset_row(self, row_id=-1):
        row_id = self.row_id if row_id == -1 else row_id
        self.cursor.execute(reset_row + str(row_id), values)
        self.db.commit()


# insert command
"""'''INSERT INTO stats(money, health, experience, lvl, active_enemies, inventory, curr_room, 
        curr_world, last_saved, if_new) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''"""
# reset row
"""'''UPDATE stats SET money = ?, health = ?, experience = ?, lvl = ?, active_enemies = ?, 
        inventory = ?, curr_room = ?, curr_world = ?, last_saved = ?, if_new = ? WHERE id = ''' + str(self.row_id)"""
