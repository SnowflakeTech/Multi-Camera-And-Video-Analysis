from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def line_to_dict(line):
    tokens = line.strip().split()
    return {
        "camera_id": int(tokens[0]),
        "obj_id": int(tokens[1]),
        "frame_id": int(tokens[2]),
        "bbox": {
            "xmin": int(tokens[3]),
            "ymin": int(tokens[4]),
            "width": int(tokens[5]),
            "height": int(tokens[6])
        },
        "gps": {
            "xworld": float(tokens[7]),
            "yworld": float(tokens[8])
        }
    }

with open("sample_tracking_data.txt", "r") as f:
    for line in f:
        data = line_to_dict(line)
        producer.send("tracking_topic", value=data)
        print(f"[Producer] Sent: {data}")
        time.sleep(0.05)  # mô phỏng real-time stream
