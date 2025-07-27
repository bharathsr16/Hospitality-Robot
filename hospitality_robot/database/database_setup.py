import sqlite3

def setup_database():
    conn = sqlite3.connect('hospitality_robot/database/events.db')
    c = conn.cursor()

    # Create table
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            description TEXT
        )
    ''')

    # Insert sample data
    events = [
        (1, 'Tech Talk', 'Auditorium', '2025-08-01 10:00:00', '2025-08-01 11:00:00', 'A talk on the future of AI.'),
        (2, 'Coding Workshop', 'Block B, Room 201', '2025-08-01 11:30:00', '2025-08-01 13:30:00', 'A hands-on workshop on Python programming.'),
        (3, 'Project Expo', 'Exhibition Hall', '2025-08-01 14:00:00', '2025-08-01 17:00:00', 'Showcase of final year student projects.'),
        (4, 'Cultural Night', 'Open Air Theatre', '2025-08-01 18:00:00', '2025-08-01 20:00:00', 'A night of music and dance performances.')
    ]

    c.executemany('INSERT OR IGNORE INTO events VALUES (?,?,?,?,?,?)', events)

    conn.commit()
    conn.close()
    print("Database setup complete and populated with sample data.")

if __name__ == '__main__':
    setup_database()
