import sqlite3
import pika

credentials = pika.PlainCredentials('test', 'test')
parameters = pika.ConnectionParameters('155.41.124.90', credentials=credentials) 

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

conn = sqlite3.connect('appStore.db')
c = conn.cursor()
#c.execute("ALTER TABLE apps ADD COLUMN status TEXT")
#c.execute("ALTER TABLE apps ADD COLUMN rdate TEXT")

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
	message = body.decode('ascii')
	print(message)
	appFeatures = message.split("/")
	if len(appFeatures)== 3:
		c.execute("UPDATE apps SET status=?,rdate=? WHERE appID =?",(appFeatures[1],appFeatures[2],appFeatures[0]))
	else:
		c.execute("UPDATE apps SET status=?,rdate=? WHERE appID =?",(appFeatures[1],None,appFeatures[0]))
	
	conn.commit()


	ch.basic_ack(delivery_tag = method.delivery_tag)
	


channel.queue_declare(queue='respond_queue', durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='respond_queue')

channel.start_consuming()
c.close()
conn.close()