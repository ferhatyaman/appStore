import pika,urllib.request
import time, sqlite3
from bs4 import BeautifulSoup
import random
from urllib.error import URLError, HTTPError

def read(id):
    success= False
    while not success:
        try:
            url = "https://itunes.apple.com/us/app/id"+ str(id) +"?mt=8"
            page = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(page,'html.parser')
            status = soup.find(class_ ='release-date')
            lastDate = status.contents[1].string
            status = status.contents[0].contents[0]
            res = "AppID: {}    Status: {}      Date: {} \n".format(str(id),status,lastDate)
            return res
            success= True
        except HTTPError as e:
            time.sleep(random.random()*3)
            success =False
        except URLError as e:
            time.sleep(random.random()*3)
            success =False
        except AttributeError:
            status = "Deleted"
            return "{}/{}".format(str(id),status)
            success = True

conn = sqlite3.connect('appStore.db')
c = conn.cursor()

credentials = pika.PlainCredentials('test', 'test')
parameters = pika.ConnectionParameters('155.41.124.90', credentials=credentials) 

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % int(body))
    res = read(int(body))
    channel.basic_publish(exchange='',routing_key='respond_queue',
                          body=str(res),
                          properties=pika.BasicProperties(
                          delivery_mode = 2, # make message persistent
                          ))
    ch.basic_ack(delivery_tag = method.delivery_tag)
	


channel.queue_declare(queue='respond_queue', durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='task_queue')

channel.start_consuming()
c.close()
conn.close()
