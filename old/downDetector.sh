#!/bin/bash

#downDetector.sh
#Author: DataFrogman

#checks the status of challenges via autosolve scripts/binaries or via expected challenge
#responses, ssh's into the challenge box, kill the docker image, then redeploys if they are
#down

#Function to check if misdirection is up and putting out the first flag component
misdirection () {
	{ 
		#fetch the output of the chal
		result=$( curl -s 10.0.0.131:5000 )
	}
	#Hardcoded correct output of the curl
	misdirectionString="<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2 Final//EN\">
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to target URL: <a href=\"/R\">/R</a>.  If not click the link."
	#fetch the current time for logging purposes
	currTime=$( date )
	#compare the fetched output with the correct output
	if [ "$misdirectionString" == "$result" ]
	then
		#if correct update the logfile
		echo "$currTime Misdirection is up" >> /home/ubuntu/logFile
	else
		#if the chal is not responding correctly update logfile
		echo "$currTime Misdirection is down" >> /home/ubuntu/logFile
		echo "$currTime Bringing up Misdirection" >> /home/ubuntu/logFile
		#ssh into the box using the ssh creds for the infra, cd into the chal git directory,
		#take docker down incase the challenge is running but vandalized, relaunch the docker
		#instance
		ssh -i ~/.ssh/CTF2019 ubuntu@10.0.0.131 'cd misdirection; docker-compose down; docker-compose up -d'
	fi

}

#This challenge has two failure states, instead of writing the relaunch twice I implemented another
#function to handle it for me
scottDown () {
	#Fetch current time for the log file
	currTime=$( date )
	#update the logfile
	echo "$currTime Bringing up Scott" >> /home/ubuntu/logFile
	#ssh into the box using the ssh creds for the infra, cd into the chal git directory, take
	#docker down in case the challenge is running but vandalized, relaunch the docker instance
	ssh -i ~/.ssh/CTF2019 ubuntu@10.0.0.64 'cd scott-web-challenge/; sudo docker-compose down; sudo docker-compose up -d'
}

#function to autosolve the "my first api" challenge and check if all components are working properly
scott () {
	{
		#fetch the initial JWT from the challenge
		initialJWT=$( curl -s http://10.0.0.64:3000/auth?name=scott )
	}
	#fetch the current time for logging
	currTime=$( date )
	#set the expected JWT opening
	jwtOpening='{"token":"'
	#check if the retrieved JWT has the correct opening
	if [ "$jwtOpening" == "$( echo $initialJWT | cut -c1-10 )" ]
	then
		#if the JWT is correct update the logfile
		echo "$currTime Scott auth is up" >> /home/ubuntu/logFile
	else
		#if the JWT is incorrect update the logfile and call the reset function
		echo "$currTime Scott auth is down" >> /home/ubuntu/logFile
		scottDown
	fi

	#fetch the solve JWT from the solve script
	adminJWT=$( node exploit.js )
	#get the flag from the challenge with the solve JWT
	flag=$( curl -s -X GET -H "Authorization: $adminJWT" http://10.0.0.64:4000/api/admin )
	#check if the flag is correct
	if [ "$flag" == '{"flag":"RITSEC{JWT_th1s_0ne_d0wn}"}' ]
	then
		#if it is correct update logfile
		echo "$currTime Scott api is up" >> /home/ubuntu/logFile
	else
		#if it is incorrect update logfile and call the reset function
		echo "$currTime Scott api is down" >> /home/ubuntu/logFile
		scottDown
	fi
}

#Initial function for jit-calc for when it was incorrectly deployed 
jit-calc () {
	{
		initialNC=$( echo "3\n" | nc ctfchallenges.ritsec.club 8000 )
	}
	currTime=$( date )
	if [ "$(echo $initialNC | cut -c1-34 )" == "Welcome to our super fast JIT calc" ]
	then
		echo "$currTime jit-calc is up" >> /home/ubuntu/logFile
	else
		echo "$currTime jit-calc is down" >> /home/ubuntu/logFile
		echo "$currTime Bringing up jit-calc" >> /home/ubuntu/logFile
		ssh -i ~/.ssh/CTF2019 ubuntu@10.0.0.129 'cd ctf_xinetd; sudo docker kill $(sudo docker ps -q); sudo docker run -d --rm -p "0.0.0.0:8000:8000" -h "jit-calc" --name="jit-calc" jit-calc'
	fi
}

#check function for the random challenge
#WARNING: this occasionally has false positives depending on the runtime due to the nature
#of the challenge
random () {
	{
		#grab the output of the solve binary and pipe it into netcat
		result=$( ./randomSolve | nc ctfchallenges.ritsec.club 8001 )
	}
	#fetch teh current time for logging purposes
	currTime=$( date )
	#extract the flag from the successful challenge output
	flag=${result: -32}
	#Check if the flag matches the correct flag
	if [ "$flag" == 'RITSEC{404_RANDOMNESS_NOT_FOUND}' ]
	then
		#if the flag is correct update logfile
		echo "$currTime random is up" >> /home/ubuntu/logFile
	else
		#if it is incorrect update the logfile
		echo "$currTime random is down" >> /home/ubuntu/logFile
		echo "$durrTime Bringing up random" >> /home/ubuntu/logFile
		#ssh into the machine using the ctf infra key, cd into the git directory, 
		#kill all running docker images incase there are any running but vandalised,
		#redeploy the docker instance
		ssh -i ~/.ssh/CTF2019 ubuntu@10.0.0.101 'cd ctf_xinetd; sudo docker kill $(sudo docker ps -q); sudo docker run -d --rm -p "0.0.0.0:8001:8001" -h "random" --name="random" random'
	fi
}

#function for the hop-by-hop challenge
hop () {
	{
		#fetch teh results of the autosolve functions
		result=$(python3 hopTest.py)
	}
	#fetch the current time for logging
	currTime=$( date )
	#check the output of the autosolve against the correct output
	if [ "$result" == "working" ]
	then
		#if it is correct update logfile
		echo "$currTime hop is up" >> /home/ubuntu/logFile
	else
		#if the challenge is not successfully solved update the logfile
		echo "$currTime hop is down" >> /home/ubuntu/logFile
		echo "$currTime Bringing up hop" >> /home/ubuntu/logFile
		#ssh into the box using the ctf ifra key, cd into the git directory, take down 
		#docker in case the image is up but vandalised, bring the docker image back up
		ssh -i ~/.ssh/CTF2019 ubuntu@10.0.0.207 'cd hop-by-hop; sudo docker-compose down; sudo docker-compose up -d'
	fi
}

#Function to check the the status of emmaunel, I do not have an autosolve so it just checks if
#is up and if it is majorly vandalized
emmaunel () {
	{
		#fetch the webpage running on the challenge
		result=$(curl -s 10.0.0.191:8003)
	}
	#fetch the current time for logging
	currTime=$( date )
	#Set the expected start of the curl response
	emmaunelString='<article> <link rel="stylesheet" type="text/css" href="style.css"> <a href="https://twitter.com/RITSECclub" target="_blank">'
	
	#check if the curl response matches the expected start
	if [ "$emmaunelString" == "$( echo $result | cut -c1-124 )" ]
	then
		#if it is correct update the logfile
		echo "$currTime emmaunel is up" >> /home/ubuntu/logFile
	else
		#if it is incorrect update the logfile
		echo "$currTime emmaunel is down" >> /home/ubuntu/logFile
		echo "$currTime Bringing up emmaunel" >> /home/ubuntu/logFile
		#ssh into the box using the infra ssh key, cd into the git directory, kill all running
		#docker images in case it is up but vandalized, redeploy the docker image
		ssh -i ~/.ssh/CTF2019 ubuntu@10.0.0.191 'cd Vulnerable-webapp; sudo docker kill $(sudo docker ps -q); sudo docker container run --name emmaunel --rm -d -p 8003:80 emmaunel'
	fi
}

#Function to check the status of jit-calc 2 via autosolve
jit2 () {
	{
		#fetch the result of the autosolve script
		result=$(python3 jit-calc-2.py)
	}
	#fetch the current time for logging
	currTime=$( date )
	#Set the expected flag
	flag=$'RITSEC{J1T_c@n_G3t_3v3n_H@rd3r}'
	
	#check if the result of the solve matches the flag
	if [ "$flag" == "$(echo $result | cut -c1017-1047)" ]
	then
		#if it is correct update the log file
		echo "$currTime Jit2 is up" >> /home/ubuntu/logFile
	else
	#if it is incorrect update the logfile
		echo "$currTime Jit2 is down" >> /home/ubuntu/logFile
		echo "$currTime Bringing up Jit2" >> /home/ubuntu/logFile
		#ssh into the box using the infra ssh key, cd into the git directory, kill all running
		#docker images in case it is up but vandalized, redeploy the docker image
		ssh -i ~/.ssh/CTF2019 ubuntu@10.0.0.174 'cd jit-calc2; sudo docker kill $(sudo docker ps -q); sudo docker run -ti -d -p 9000:9000 --privileged 3aa06547d920'
	fi


}

#Call the working functions here, comment out if you are doing any major repairs on a function
#so that downDetector does not nuke any of your docker images
emmaunel
hop
random
misdirection
scott
#jit-calc
#jit2
