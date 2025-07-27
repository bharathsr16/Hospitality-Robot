import sqlite3

def get_event_details(event_name):
    """
    Retrieves the details of an event from the database.
    """
    conn = sqlite3.connect('hospitality_robot/database/events.db')
    c = conn.cursor()
    c.execute("SELECT * FROM events WHERE name LIKE ?", ('%' + event_name + '%',))
    event = c.fetchone()
    conn.close()
    return event

def get_all_events():
    """
    Retrieves all events from the database.
    """
    conn = sqlite3.connect('hospitality_robot/database/events.db')
    c = conn.cursor()
    c.execute("SELECT * FROM events")
    events = c.fetchall()
    conn.close()
    return events

if __name__ == '__main__':
    print("All events:")
    print(get_all_events())
    print("\nDetails for 'Tech Talk':")
    print(get_event_details('Tech Talk'))
