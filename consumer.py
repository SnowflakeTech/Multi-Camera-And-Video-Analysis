from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'tracking_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='tracker_group'
)

latest_tracks = []

def consume_messages():
    for message in consumer:
        data = message.value
        latest_tracks.append(data)
        if len(latest_tracks) > 1000:
            latest_tracks.pop(0)
