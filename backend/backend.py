import sqlite3
from ai_engine import process_image

DB_PATH = ../database/safehouse.db
// повідомлення для ксюші:  ти зробила 2 моделі ШІ. lp ти перевірила, працює на 60% добре я б сказала, 
// походу треба дотреновувати. ocr не перевіряла, бо там ніби то те що перевірене lp це просто фотки з
// рамочкою навколо номерного знаку, а треба витягнути прям crop знаку. для цього треба дотренувати модель
// і налаштувати crop (можливо уже, дивись ai_engine, я не читала). зараз я намагаюсь поєднати роботу бд і ші.
// тому я зупинилась на тому що створила ai_engine та backend.py.



def log_to_database(plate_text, img_path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM vehicles WHERE license_plate = ?", (plate_text,))
    vehicle = cursor.fetchone()

    if vehicle:
        match_status = 'registered'
        vehicle_id = vehicle[0]
    else:
        match_status = 'unregistered'
        vehicle_id = None

    cursor.execute("""
        INSERT INTO detection_logs 
        (checkpoint_id, user_id, direction, recognized_plate, vehicle_id, match_status, photo_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (1, 1, 'in', plate_text, vehicle_id, match_status, img_path))

    conn.commit()
    conn.close()
    print(f"Added. Number: {plate_text}, Status: {match_status}")

if __name__ == "__main__":
    test_photo = ../ai_processing/UC3M-LP/test/00000.jpg"
    
    recognized_text = process_image(test_photo)
    
    if recognized_text:
        log_to_database(recognized_text, test_photo)
    else:
        print("Didn`t found")