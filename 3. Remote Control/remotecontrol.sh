#!/bin/bash

#Part 1: This portion of the code checks if the required applications are installed.   (geoip-bin, tor, sshpass, nipe) 
#If the applications are not found in the system, they will be installed.                
#Otherwise, a message will indicate that the application has already been installed.

sudo apt-get -qq update

if [ "$(apt-cache policy geoip-bin | grep Installed | sed 's/^.*: //')" == '(none)' ]
then
	sudo apt-get install -y geoip-bin
else
	echo '[#] geoip-bin is already installed.'
fi

if [ "$(apt-cache policy tor | grep Installed | sed 's/^.*: //')" == '(none)' ]
then
	sudo apt-get install -y tor
else
	echo '[#] tor is already installed.'
fi

if [ "$(apt-cache policy sshpass | grep Installed | sed 's/^.*: //')" == '(none)' ]
then
	sudo apt-get install -y sshpass
else
	echo '[#] sshpass is already installed.'
fi

if [ "$(ls | grep nipe)" == 'nipe' ]
then
	echo '[#] nipe is already installed.'
else
	git clone https://github.com/htrgouvea/nipe && cd nipe
	sudo apt-get install -y cpanminus
	cpanm --installdeps .
	sudo cpanm install Switch JSON LWP::UserAgent Config::Simple
	sudo perl nipe.pl install
fi

#Part 2: This portion of the code connects the machine to the Tor network via nipe. 
#If connection to nipe is successful and anonymous, the spoofed IP and Country will be displayed.
#If connection fails, the script will alert the user and exit. 

cd ~/nipe

sudo perl nipe.pl restart

anonip=$(sudo perl nipe.pl status | grep Ip | awk '{print$3}')

if [ "$(sudo perl nipe.pl status | grep Status | awk '{print$3}')" == "true" ]
then
	echo "[*] You are anonymous..Connecting to the remote Server."
	echo
	echo "[*] Your spoofed IP address is: $anonip, Spoofed country: $(geoiplookup $anonip | grep , | sed 's/^.*, //')"
else
	echo '[-] You are unable to connect anonymously, exiting script.'
	exit
fi

#Part 3: Get user input for Domain/IP to scan

echo -n '[?] Specify a Domain/IP address to scan: ' ; read doip
echo

#Part 4: Connect automatically to remote server, and display details of the remote server (uptime, IP and country) 
#The Domain/IP given by user is scanned and data is appended into a file 'whois_doip'
#The file is then transferred into your local machine using FTP
#REPLACE 'tc' in the variables with the username(under 'user' variable) and password(under 'pw' variable) to your remote server!

user=tc
pw=tc
remote=192.168.163.129

sshpass -p $pw ssh -q -t -o StrictHostKeyChecking=no $user@$remote "echo '[*] Connecting to remote server:'
echo -n "Uptime:" && uptime 
echo "IP Address: $remote"
echo "Country: $(whois $remote | grep -i country | awk '{print$2}')"
echo

whois $doip >> whois_doip .
echo "[*] Extracting data using whois on Domain/IP address of victim"
echo "[@] whois data is saved into /home/kali/nipe/whois_doip"
exit"

curl -s -u tc:tc -O ftp://$remote/whois_doip

#Part 5: A log file is prepared, for the scanned whois data. The data is appended into 'nr.log'
echo "$(date) $(echo "[*] whois data collected for: $doip")" >> nr.log
