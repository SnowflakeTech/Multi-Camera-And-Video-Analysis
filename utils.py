import cv2
import numpy as np
from PIL import Image

# Load ảnh nền hoặc video frame mô phỏng
# background = cv2.imread("/background.jpg")

def draw_bbox(data, base_img):
    img = base_img.copy()
    x = data['bbox']['xmin']
    y = data['bbox']['ymin']
    w = data['bbox']['width']
    h = data['bbox']['height']
    obj_id = data['obj_id']
    cam = data['camera_id']

    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(img, f'ID:{obj_id}-C{cam}', (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)
    return img

def generate_heatmap(coords, base_img):
    heat = np.zeros((base_img.shape[0], base_img.shape[1]), dtype=np.float32)
    for pt in coords:
        x = int(pt[0])
        y = int(pt[1])
        if 0 <= y < heat.shape[0] and 0 <= x < heat.shape[1]:
            heat[y, x] += 1

    heat = cv2.GaussianBlur(heat, (41, 41), 0)
    heatmap_img = cv2.applyColorMap(np.uint8(255 * heat / heat.max()), cv2.COLORMAP_JET)
    combined = cv2.addWeighted(base_img, 0.6, heatmap_img, 0.4, 0)
    return combined

def detect_anomaly(data):
    # Ví dụ: cảnh báo khi bounding box quá nhỏ hoặc tọa độ nhảy mạnh
    w, h = data['bbox']['width'], data['bbox']['height']
    if w * h < 500:
        return "❗ Đối tượng nhỏ bất thường"
    return None
