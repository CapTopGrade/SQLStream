from kafka import KafkaConsumer
from collections import Counter
import json
import time

consumer = KafkaConsumer(
    'website_events',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

event_counts = Counter()
start_time = time.time()

while True:
    messages = consumer.poll(timeout_ms=1000)
    for _, msg_list in messages.items():
        for msg in msg_list:
            event = msg.value
            key = (event['event_type'], event.get('product', 'none'))  # Используем кортеж для учёта продукта
            event_counts[key] += 1
    elapsed = time.time() - start_time
    if elapsed >= 300:  # 5 минут
        print(f"Results after 5 minutes: {dict(event_counts)}")
        event_counts.clear()
        start_time = time.time()
    time.sleep(1)