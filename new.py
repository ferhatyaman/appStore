import urllib.request
from bs4 import BeautifulSoup
import string, sys, subprocess, shlex

f = open("urls.txt", "r")
for line in f:
	cmd = "qsub -q bme.q -cwd qsub-job.sh {}".format(line)
	args = shlex.split(cmd)
	result = subprocess.run(args,stdout=subprocess.PIPE)
	result.stdout