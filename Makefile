SHELL=/bin/bash

setup:
	pip install -r requirements.txt

run:
	source .env && flask run

# establish an SSH tunnel to the MySQL server
ssh.up:
	source .env && ssh -NfL $${MYSQL_PORT}:$${MYSQL_LOCAL_HOST}:$${MYSQL_PORT} $${MYSQL_USER}@$${SSH_HOST}

ssh.down:
	kill $$(ps aux | grep ssh | grep -v grep | tr -s ' ' | cut -d' ' -f2)

ssh.renew:
	make ssh.down
	make ssh.up