# init_db.py
import sqlite3

def init_db():
    conn = sqlite3.connect('cpl.db')
    cursor = conn.cursor()

    # Create Teams Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Teams (
            team_id INTEGER PRIMARY KEY,
            team_name TEXT,
            color TEXT,
            points INTEGER
        )
    ''')

    # Insert your Teams
    cursor.execute("INSERT OR IGNORE INTO Teams (team_id, team_name, color, points) VALUES (1, 'Royal Challengers', 'red', 100)")
    cursor.execute("INSERT OR IGNORE INTO Teams (team_id, team_name, color, points) VALUES (2, 'Super Kings', 'yellow', 100)")
    cursor.execute("INSERT OR IGNORE INTO Teams (team_id, team_name, color, points) VALUES (3, 'Sun Risers', 'orange', 100)")

    # Create Players Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Players (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            team_id INTEGER,
            no_bid INTEGER DEFAULT 0,
            FOREIGN KEY (team_id) REFERENCES Teams(team_id)
        )
    ''')

    # Insert your Players
    players = [
        ('Maari',), ('Jaya',), ('Sidhu',), ('Ajay',), ('Vijay',),
        ('sudheer',), ('vishnu',), ('Hari',), ('Hemanth',), ('Nanai',),
        ('kiran',), ('Chintu',), ('Uday',), ('Manoj',), ('Masthan',),
        ('Chotu',), ('Suresh anna',), ('Sumanth',), ('Mani Anna',)
    ]

    cursor.executemany("INSERT OR IGNORE INTO Players (name) VALUES (?)", players)

    conn.commit()
    conn.close()
    print("Database created and initialized with your data.")

if __name__ == "__main__":
    init_db()
