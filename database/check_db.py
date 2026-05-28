import sqlite3
import os

db_name = "safehouse.db"

if not os.path.exists(db_name):
    print(f"Error: File {db_name} not found. Please run init_db.py and seed_db.py first.")
    exit()

# Connect to the database
conn = sqlite3.connect(db_name)
# Use sqlite3.Row to easily access column names
conn.row_factory = sqlite3.Row 
cursor = conn.cursor()

print("="*60)
print("DATABASE INSPECTION: safehouse.db")
print("="*60)

# Fetch all table names from the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
tables = cursor.fetchall()

if not tables:
    print("The database is empty (no tables found).")
else:
    for table_row in tables:
        table_name = table_row['name']
        print(f"\n--- TABLE: {table_name.upper()} ---")
        
        # Fetch all records from the current table
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        if not rows:
            print("(Table is empty)")
            continue
            
        # Print column names
        col_names = [description[0] for description in cursor.description]
        header = " | ".join(col_names)
        print(header)
        print("-" * len(header))
        
        # Print each row's data
        for row in rows:
            # Convert all values to strings and handle NULL (None) values
            row_data = [str(row[col]) if row[col] is not None else "NULL" for col in col_names]
            print(" | ".join(row_data))

print("\n" + "="*60)
print("End of database inspection.")
print("="*60)

conn.close()