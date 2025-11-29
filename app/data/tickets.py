from app.data.db import connect_database

def insert_ticket(ticket_id, priority, status, category, subject, description, created_date, assigned_to=None):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets
        (ticket_id, priority, status, category, subject, description, created_date, assigned_to)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, priority, status, category, subject, description, created_date, assigned_to))
    conn.commit()
    lastid = cursor.lastrowid
    conn.close()
    return lastid

def get_all_tickets():
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM it_tickets ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_ticket_status(ticket_id, new_status):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE it_tickets SET status = ? WHERE ticket_id = ?", (new_status, ticket_id))
    conn.commit()
    count = cursor.rowcount
    conn.close()
    return count
