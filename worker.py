#!/usr/bin/env python
import pika
import time, sqlite3
from pexpect import pxssh
import getpass

try:
    s = pxssh.pxssh()
    hostname = "enggrid.bu.edu"
    username = "fyaman"
    password = getpass.getpass('password: ')
    s.login(hostname, username, password)
    s.sendline('qlogin')
    s.prompt()
    s.sendline('yes')
    s.prompt()
    s.sendline('cd /mnt/nokrb/fyaman/')
    s.prompt()
    print(s.before)	 # print everything before the prompt.
    s.sendline('module load anaconda/3.4')
    s.prompt()


    print(s.before)
except pxssh.ExceptionPxssh as e:
    print("pxssh failed on login.")
    print(e)








conn = sqlite3.connect('appStore.db')
c = conn.cursor()

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
	print(" [x] Received %r" % int(body))
	print(body)
	
	ch.basic_ack(delivery_tag = method.delivery_tag)
	
	s.sendline('python3 appInfo.py {}'.format(int(body)))
	s.prompt()
	print(s.before)
	print("\n")
	s.prompt()



channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='task_queue')

channel.start_consuming()
c.close()
conn.close()

s.sendline('exit')
s.prompt()
s.logout()