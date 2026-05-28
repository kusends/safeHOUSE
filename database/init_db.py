import sqlite3  
import os

db_name = "safehouse.db"

sql_script = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT CHECK(role IN ('guard', 'admin')) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);

CREATE TABLE IF NOT EXISTS checkpoints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    camera_ip TEXT,
    detector_status BOOLEAN DEFAULT 1
);

CREATE TABLE IF NOT EXISTS owners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone_number TEXT,
    address TEXT
);

CREATE TABLE IF NOT EXISTS vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    license_plate TEXT UNIQUE NOT NULL,
    owner_id INTEGER REFERENCES owners(id) ON DELETE SET NULL,
    brand_model TEXT,
    status TEXT CHECK(status IN ('active', 'flagged')) DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS detection_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    checkpoint_id INTEGER REFERENCES checkpoints(id) ON DELETE SET NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    direction TEXT CHECK(direction IN ('in', 'out')) NOT NULL,
    recognized_plate TEXT,
    vehicle_id INTEGER REFERENCES vehicles(id) ON DELETE SET NULL,
    match_status TEXT CHECK(match_status IN ('registered', 'unregistered', 'unreadable')) NOT NULL,
    photo_path TEXT
);
"""

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

cursor.executescript(sql_script)

conn.commit()
conn.close()

print(f"Database was created. Path to the file: {os.path.abspath(db_name)}")