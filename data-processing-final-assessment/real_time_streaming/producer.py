from kafka import KafkaProducer
import json, time, random

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

while True:
    data = {"sensor_id": random.randint(1,5),
            "temperature": random.uniform(20, 40),
            "humidity": random.uniform(30, 80)}
    producer.send('sensor_data', value=data)
    print("Produced:", data)
    time.sleep(1)
