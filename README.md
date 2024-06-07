# Cybersecurity Projects
1. Network Mapping:
Mapped a home network and identified all connected devices using the router’s web interface.

2. Info Extractor:
Developed a bash script to automatically extract system information from a user's machine, including the IP and MAC addresses, memory usage on the CPU and the largest files in the system. An unknown process that results in unusually high memory usage on the CPU could indicate that the machine has been compromised by attackers.

3. Remote Control:
Developed a bash script to automate the scanning of a domain anonymously using the Tor network. The script first connects the user's machine to the Tor network to spoof the user's IP address, thereafter connecting to a remote server via sshpass and then scanning a domain of interest. The information from the scanning is then appended into a log file.

4. Log Analyzer:
Developed a python script that automatically parses auth.log files on Linux, extracting essential information from the log file that could indicate a potential security breach in the network. The information extracted include details on adding and deleting users, changes in user passwords and the use of sudo and su command.
