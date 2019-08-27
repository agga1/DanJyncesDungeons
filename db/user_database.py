import sqlite3

db = sqlite3.connect('data/test_db')
CREATE_TABLE = '''
    CREATE TABLE stats(id INTEGER PRIMARY KEY, money INTEGER, health INTEGER, inventory TEXT)
'''
cursor = db.cursor()
cursor.execute(CREATE_TABLE)
db.commit()

def insert(): # create new row with new game instance
    cursor.execute('''INSERT INTO stats(money, health, inventory)
    VALUES(0, 0, "")
                
    ''')

# def update_money(row_id, money):




