from flask import Flask, render_template, request
from kafka import KafkaProducer
import json
import time

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def send_event(event_type, page, product=None):
    event_data = {
        "event_type": event_type,
        "page": page,
        "product": product if product else None,
        "ts": int(time.time() * 1000)
    }
    producer.send('website_events', event_data)
    print(f"Sent event: {event_data}")

@app.route('/')
def home():
    send_event("view", "/home")
    return render_template('home.html')

@app.route('/shop')
def shop():
    send_event("view", "/shop")
    return render_template('shop.html')

@app.route('/products')
def products():
    send_event("view", "/products")
    return render_template('products.html')

@app.route('/click')
def click():
    product = request.args.get('product')  # Получаем параметр продукта, если есть
    send_event("click", "/products", product=product)
    return "Click recorded!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)