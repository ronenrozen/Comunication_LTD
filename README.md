# Prerequisets:
	*Node.Js
	*openssl
	*python 3.7
	

Preparing server (do this commands in server folder) -<br/> <br/> 
	1.create env, run this command in cli - python -m venv my_venv<br/>
	2.install requierments , pip install -r requierments.txt<br/>
	3.generate Openssl certificate with this command- <br/>
	openssl req -nodes -x509 -newkey rsa:2048 -keyout ca.key -out ca.crt -subj "/C=IL/L=Israel/OU=root/CN=`localhost -		f`/emailAddress=comunication.LTD@gmail.com"<br/>
	3. in cli - python run.py<br/>

Preparing client (do this commands in client folder) -<br/><br/> 
	1.run - npm install<br/>
	2.run npm start<br/>
	
	
Now the server and the client are running. <br/>
Go to https://localhost:3000<br/>
admin user<br/>
	email - admin@admin.com<br/>
	password - admin<br/>
	
# Docker
	Just use - docker-compose up --build<br/>
	**IMPORTANT before running above command generate certificate
	
client - http://localhost:3000
server - https://localhost:5000
