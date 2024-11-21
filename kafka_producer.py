from confluent_kafka import Producer
import json

conf = {
    'bootstrap.servers': "localhost:9092",  
    'client.id': 'location_producer',  
}

producer = Producer(conf)

def delivery_report(err, msg):
    """Callback function to handle delivery reports"""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to: {msg.topic()}[{msg.partition()}]")

def send_like_event(post_id):
    """Send a like event to Kafka topic"""
    try:
        # sends data to consumer in json format
        message = json.dumps({"post_id": post_id}).encode('utf-8')
        
        # Send message to Kafka consumer
        producer.produce(
            topic='like_topic',
            key=str(post_id).encode('utf-8'),  # Encode key as bytes
            value=message,
            callback=delivery_report
        )
        print("Message sent to Kafka")
        producer.poll(0)  # Trigger delivery reports
        
    except BufferError:
        print("Local producer queue is full")
        producer.poll(0.1)  # Flush queue
    except Exception as e:
        print(f"Error sending message: {str(e)}")
    finally:
        producer.flush()  # Ensure all messages are delivered

# Example usage
if __name__ == "__main__":
    send_like_event("1")
