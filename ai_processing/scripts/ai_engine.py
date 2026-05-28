from ultralytics import YOLO
import cv2

LP_MODEL_PATH = ../cfg/runs/detect/lp_model-3/weights/best.pt
OCR_MODEL_PATH = ../cfg/runs/detect/ocr_model/weights/best.pt

def process_image(img_path):
    lp_model = YOLO(LP_MODEL_PATH)
    ocr_model = YOLO(OCR_MODEL_PATH)

    img = cv2.imread(img_path)
    if img is None:
        return None

    lp_results = lp_model(img, verbose=False)
    
    if not lp_results[0].boxes:
        return None

    box = lp_results[0].boxes[0]
    x1, y1, x2, y2 = map(int, box.xyxy[0])
    plate_crop = img[y1:y2, x1:x2]

    ocr_results = ocr_model(plate_crop, verbose=False)
    
    chars = []
    for ocr_box in ocr_results[0].boxes:
        char_x1 = int(ocr_box.xyxy[0][0])
        class_id = int(ocr_box.cls[0])
        char_name = ocr_model.names[class_id]
        chars.append((char_x1, char_name))
    
    chars.sort(key=lambda x: x[0])
    return "".join([c[1] for c in chars])