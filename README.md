This project is about pull specific information of  all applications on iTunes. This proccess has several step. It also has severeal requirements before run.

Requirements:
1-There should be rabbitmq-server on your server or your localhost.(However this is long-running process. If there is a static ip server or if connection on the localhost is not break, you can use this server.)
2-New user should be added for credential on rabbitmq management system.
3-There should be a grid-system which has 50-100 cluster which has anaconda module.

Steps:
1- Install rabbitmq and start the server
2- Run the appReader.py which creates appStore.db database which has information of apps.
Note: this step may take 7-8 hours to execute. Be patient.
Note: I also upload an example database which has 1.3 million app id 
3- After Step 2 done, Run the new_task.py which sends information rabbitmq server.
4- Run the worker.py on clusters
	a- Download environment.yml, appStore.sh, Makefile, worker.py on your cluster workspace.
	b- Run 'make' command how many cluster you want to work
5- After Step 3 done, Run read_responds.py which updates appStore.db which you created on Step 2

After all steps, information of application is ready.

Specific Case:(Margherita)
	Static IP: 128.197.176.242
	Rabbitmq Credentials:
		user: foo
		password: bar

	Create a virtual environment for python codes