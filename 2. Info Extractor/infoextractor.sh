#!/bin/bash

#this command displays the public IP address of your network
echo "Your Public IP is $(curl -s ifconfig.io)"
echo
sleep 2

#this command displays the private IP address of your machine
echo "Your Private IP is $(ifconfig | grep broadcast | awk '{print$2}')"
echo
sleep 2

#this command displays the MAC address of your machine
echo "Your MAC address is XX:XX:XX:$(cat /sys/class/net/*/address | 
head -n 1 | awk '{print substr($0, length($0)-7)}')"
echo
sleep 2

#this command displays the top 5 processes that has the highest CPU usage
echo "The top 5 processes in terms of CPU usage:"
ps -Ao user,uid,comm,pid,pcpu,tty --sort=-pcpu | head -n 6
echo
sleep 4

#this command displays the free and used memory of your machine
echo "The memory usage on your CPU:"
free -m | head -n 2
echo
sleep 4

#this command displays the active system services and statuses
echo "The Active system services and statuses on your CPU:"
systemctl --type=service --state=active | head -n -6
echo
sleep 4

#this command displays the top 10 largest files in your /home directory
echo "The top 10 largest files from your /home directory:"
sudo find /home -type f -exec du -h {} + | sort -rh | head -n 10
