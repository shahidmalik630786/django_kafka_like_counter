from django.core.management.base import BaseCommand
from confluent_kafka import Consumer, KafkaException
import json
from collections import defaultdict
import os
from django.db import transaction, connection
from like.models import Post


class Command(BaseCommand):
    help = "This command allows us to run Kafka consumer"

    def process_batch(self, like_batch):
        '''This will store data in db when defaultdict length has store 10 records'''
        with connection.cursor() as cursor:
            with transaction.atomic():
                for post_id, like_count in like_batch.items():
                    try:
                        post = Post.objects.select_for_update().get(id=post_id)
                        post.likes += like_count
                        post.save()
                    except Post.DoesNotExist:
                        print(f"Post with ID {post_id} does not exist.")
                    except Exception as e:
                        print(f"Error processing batch: {e}")
        print(f"Batch processed: {like_batch}")

    def handle(self, *args, **options):
        """reciving the producer data"""
        conf = {
            "bootstrap.servers": "localhost:9092",
            "group.id": "location_group",
            "auto.offset.reset": "earliest"
        }
        consumer = Consumer(conf)

        consumer.subscribe(['like_topic'])  

        total_messages = 0
        like_batch = defaultdict(int)
        try:
            while True:
                print("** Listening for messages **")
                msg = consumer.poll(timeout=1.0)  
                
                if msg is None:
                    continue  

                if msg.error():
                    print(f"Error: {msg.error()}")
                    continue  
                
                try:
                    data = json.loads(msg.value().decode('utf-8'))
                except json.JSONDecodeError:
                    print(f"Error decoding JSON: {msg.value()}")
                    continue  
                
                post_id = data.get('post_id')
                #storing the data in defaultdict which is recived from producer
                if post_id:
                    like_batch[post_id] += 1
                    total_messages += 1
                else:
                    print("Missing 'post_id' in message.")
                
                print(f"like batch - {like_batch}, total_messages - {total_messages}")
                if total_messages >= 10:
                    self.process_batch(like_batch)
                    like_batch.clear()  
                    total_messages = 0

        except KeyboardInterrupt:
            print("** Kafka consumer stopped by user **")
        except KafkaException as e:
            print(f"Kafka exception occurred: {e}")
        finally:
            print("** Closing consumer **")
            consumer.close()  
