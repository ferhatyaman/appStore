#!/usr/bin/env python
import pika
import sys, sqlite3


#Before to run new_task.py, be sure 
credentials = pika.PlainCredentials('test', 'test')
parameters = pika.ConnectionParameters('155.41.64.109', credentials=credentials) 
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)



conn = sqlite3.connect('appStore.db')
c = conn.cursor()
c.execute('SELECT * FROM apps')
data = c.fetchall()
for row in data:
	channel.basic_publish(exchange='',routing_key='task_queue',
	                      body=str(row[0]),
	                      properties=pika.BasicProperties(
	                      delivery_mode = 2, # make message persistent
	                      ))




print(" [x] Sent")
connection.close()