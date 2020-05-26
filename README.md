Prerequisets:
Install
	*Node.Js
	*openssl
	*python 3.7
	

Preparing server (do this commands in server folder) - 
	1.create env, run this command in cli - python -m venv my_venv
	2.install requierments , pip install -r requierments.txt
	3.generate Openssl certificate with this command- 
		openssl req -nodes -x509 -newkey rsa:2048 -keyout ca.key -out ca.crt -subj "/C=IL/L=Israel/OU=root/CN=`localhost -f`/emailAddress=comunication.LTD@gmail.com"
	3. in cli - python run.py

Preparing client (do this commands in client folder)
	1.run - npm install
	2.run npm start
	
	
Now the server and the client are running. 
Go to https://localhost:3000
admin user
	email - admin@admin.com
	password - admin
	
# Docker
	Just use docker-compose up --build
	client - http://localhost:3000
	server - https://localhost:5000