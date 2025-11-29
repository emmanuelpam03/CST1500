import pandas as pd
from app.data.db import connect_database

def insert_dataset_metadata(dataset_name, category, source, last_updated, record_count, file_size_mb):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata
        (dataset_name, category, source, last_updated, record_count, file_size_mb)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_name, category, source, last_updated, record_count, file_size_mb))
    conn.commit()
    lastid = cursor.lastrowid
    conn.close()
    return lastid

def load_csv_to_table(csv_path, table_name, if_exists='append'):
    import pandas as pd
    conn = connect_database()
    df = pd.read_csv(csv_path)
    df.to_sql(name=table_name, con=conn, if_exists=if_exists, index=False)
    conn.close()
    return len(df)
