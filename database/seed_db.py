import sqlite3
import os

db_name = "safehouse.db"

if not os.path.exists(db_name):
    print(f"Error: File {db_name} not found. Please run init_db.py first.")
    exit()

sql_seed_data = """
PRAGMA foreign_keys = ON;

-- 1. Add staff (Guards and Admins)
INSERT INTO users (username, password_hash, role) VALUES 
('admin_john', 'hash_qwerty123', 'admin'),
('guard_peter', 'hash_secure456', 'guard');

-- 2. Add checkpoints
INSERT INTO checkpoints (name, camera_ip, detector_status) VALUES 
('Main Entrance (North)', '192.168.1.10', 1),
('Underground Parking (South)', '192.168.1.11', 1);

-- 3. Add owners / residents
INSERT INTO owners (full_name, phone_number, address) VALUES 
('Elena Smith', '+48111222333', 'Apt 42'),
('BuildInvest LLC (Corporate)', '+48449998877', 'Office 3'),
('Mark Johnson', '+48999888777', 'Apt 12');

-- 4. Add vehicles
INSERT INTO vehicles (license_plate, owner_id, brand_model, status) VALUES 
('AA1234BB', 1, 'Toyota RAV4', 'active'),
('BC9876CX', 2, 'Ford Transit', 'active'),
('WAW1010', 3, 'Audi A6', 'active'),   
('KA0000XX', NULL, 'Unknown', 'flagged'); -- Suspicious vehicle (flagged by security)

-- 5. Add records to the detection log
-- Event 1: Guard Peter allowed a registered Toyota in
INSERT INTO detection_logs (checkpoint_id, user_id, direction, recognized_plate, vehicle_id, match_status, photo_path) 
VALUES (1, 2, 'in', 'AA1234BB', 1, 'registered', 'dataset/sample/toyota.jpg');

-- Event 2: Automatic exit of a Ford (No guard on duty -> user_id = NULL)
INSERT INTO detection_logs (checkpoint_id, user_id, direction, recognized_plate, vehicle_id, match_status, photo_path) 
VALUES (2, NULL, 'out', 'BC9876CX', 2, 'registered', 'dataset/sample/ford.jpg');

-- Event 3: Camera captured an unknown vehicle not in the database
INSERT INTO detection_logs (checkpoint_id, user_id, direction, recognized_plate, vehicle_id, match_status, photo_path) 
VALUES (1, 2, 'in', 'WX5555Y', NULL, 'unregistered', 'dataset/sample/unknown.jpg');

-- Event 4: Muddy license plate (AI failed to read)
INSERT INTO detection_logs (checkpoint_id, user_id, direction, recognized_plate, vehicle_id, match_status, photo_path) 
VALUES (1, NULL, 'in', NULL, NULL, 'unreadable', 'dataset/sample/muddy_car.jpg');
"""

try:
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.executescript(sql_seed_data)
    conn.commit()
    conn.close()
    print("Success! Database has been populated with test data.")
    
except sqlite3.IntegrityError as e:
    print(f"Warning: Test data might have already been added. Details: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")