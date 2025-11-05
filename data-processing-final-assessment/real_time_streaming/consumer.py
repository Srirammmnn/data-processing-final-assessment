from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('sensor_data',
                         bootstrap_servers=['localhost:9092'],
                         auto_offset_reset='earliest',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

for msg in consumer:
    print("Consumed:", msg.value)
