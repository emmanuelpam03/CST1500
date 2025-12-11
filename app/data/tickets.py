from app.data.db import connect_database
import pandas as pd
def migrate_tickets_from_file(file_path="DATA/it_tickets.csv"):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM it_tickets")

    if cursor.fetchone()[0] == 0:
        with open(file_path, 'r') as f:
            next(f)

            for line in f:
                parts = line.strip().split(',')

                if len(parts) != 7:
                    continue

                ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours = parts
                
                cursor.execute("""
                    INSERT INTO it_tickets
                    (ticket_id, priority, description, status, assigned_to, created_date, resolved_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours))

    conn.commit()
    conn.close()


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
    df = pd.read_sql_query("SELECT * FROM it_tickets ORDER BY id DESC", conn)
    conn.close()
    return df

def update_ticket_status(ticket_id, new_status):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE it_tickets SET status = ? WHERE ticket_id = ?", (new_status, ticket_id))
    conn.commit()
    count = cursor.rowcount
    conn.close()
    return count
