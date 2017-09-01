import pexpect
import getpass

password = getpass.getpass('password: ')

for i in range(20):
	
	child = pexpect.spawn('python3 worker.py')

	child.expect('password:')
	child.sendline(password)
	print(i)
