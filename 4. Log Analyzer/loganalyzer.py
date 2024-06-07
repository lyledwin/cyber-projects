import re
import time

file = open ("auth.log", "r")
fdata = file.readlines()

#Part 1: Details of command usage (as all commands were used with sudo, they are only printed in Part 2E)
linecounter1 = -1
for line in fdata:
	line = line.strip()
	linecounter1 += 1
	if "COMMAND=" in line and "sudo:" not in line:
		if linecounter1+1 <= len(fdata):
			if "by (" in fdata[linecounter1+1]:
				exeuser1 = re.search("(?<=by\s\()(.*?)(?=\))", fdata[linecounter1+1])
			else:
				exeuser1 = re.search("(?<=sudo:\s)(.*?)(?=\s:)", line)
		date1 = re.search("[0-9]{1,4}-[0-9]{1,2}-[0-9]{1,2}", line)
		time1 = re.search("[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}", line)
		print("EVENT TYPE: command_usage")
		if exeuser1.group() == "uid=1000":
			print("EXECUTION_USERNAME: kali")
		elif  exeuser1.group() == "uid=0":
			print("EXECUTION_USERNAME: root")
		else:
			print(f"EXECUTION_USERNAME: {exeuser1.group()}")
		if linecounter1+1 <= len(fdata):
			if "/usr/bin" in line and "by (" in fdata[linecounter1+1]:
				cmdtype1 = re.search("(?<=/usr/bin/)(.*)", line)
				print(f"COMMAND_EXECUTED: {cmdtype1.group()}")
			elif "/usr/sbin" in line and "by (" in fdata[linecounter1+1]:
				cmdtype1 = re.search("(?<=/usr/sbin/)(.*)", line)
				print(f"COMMAND_EXECUTED: {cmdtype1.group()}")
			else:
				if "/usr/bin" in line:
					cmdfailed1 = re.search("(?<=/usr/bin/)(.*)", line)
					print(f"COMMAND_EXECUTED: {cmdfailed1.group()}")
				elif "/usr/sbin" in line:
					cmdfailed1 = re.search("(?<=/usr/sbin/)(.*)", line)
					print(f"COMMAND_EXECUTED: {cmdfailed1.group()}")
				else:
					cmdfailed1 = re.search("(?<=COMMAND=)(.*)", line)
					print(f"COMMAND_EXECUTED: {cmdfailed1.group()}")
		print(f"TIMESTAMP: {date1.group()} {time1.group()}")
		if linecounter1+1 <= len(fdata):
			if "by (" not in fdata[linecounter1+1]:
				print ("COMMAND_USAGE_STATUS: FAILED")
		print(" ")
		time.sleep(3)

#Part 2A: Details of newly added users
linecounterA = -1
for line in fdata:
	line = line.strip()
	linecounterA += 1
	if "/usr/sbin/useradd" in line:
		if linecounterA+1 <= len(fdata):
			if "by (" in fdata[linecounterA+1]:
				exeuserA = re.search("(?<=by\s\()(.*?)(?=\))", fdata[linecounterA+1])
			else:
				exeuserA = re.search("(?<=sudo:\s)(.*?)(?=\s:)", line)
		newuserA = re.search("(?<=useradd\s)(.*)", line)
		dateA = re.search("[0-9]{1,4}-[0-9]{1,2}-[0-9]{1,2}", line)
		timeA = re.search("[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}", line)
		print("EVENT TYPE: new_user")
		if exeuserA.group() == "uid=1000":
			print("EXECUTION_USERNAME: kali")
		elif  exeuserA.group() == "uid=0":
			print("EXECUTION_USERNAME: root")
		else:
			print(f"EXECUTION_USERNAME: {exeuserA.group()}")
		print(f"NEW_USERNAME: {newuserA.group()}")
		print(f"TIMESTAMP: {dateA.group()} {timeA.group()}")
		if linecounterA+1 <= len(fdata):
			if "by (" not in fdata[linecounterA+1]:
				print ("NEW_USER_STATUS: FAILED")
		print(" ")
		time.sleep(3)

#Part 2B: Details of deleted users
linecounterB = -1
for line in fdata:
	line = line.strip()
	linecounterB += 1
	if "/usr/sbin/userdel" in line:
		if linecounterB+1 <= len(fdata):
			if "by (" in fdata[linecounterB+1]:
				exeuserB = re.search("(?<=by\s\()(.*?)(?=\))", fdata[linecounterB+1])
			else:
				exeuserB = re.search("(?<=sudo:\s)(.*?)(?=\s:)", line)			
		deluserB = re.search("(?<=userdel\s)(.*)", line)
		dateB = re.search("[0-9]{1,4}-[0-9]{1,2}-[0-9]{1,2}", line)
		timeB = re.search("[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}", line)
		print("EVENT TYPE: delete_user")
		if exeuserB.group() == "uid=1000":
			print("EXECUTION_USERNAME: kali")
		elif  exeuserB.group() == "uid=0":
			print("EXECUTION_USERNAME: root")
		else:
			print(f"EXECUTION_USERNAME: {exeuserB.group()}")
		print(f"DELETED_USERNAME: {deluserB.group()}")
		print(f"TIMESTAMP: {dateB.group()} {timeB.group()}")
		if linecounterB+1 <= len(fdata):
			if "by (" not in fdata[linecounterB+1]:
				print ("DELETE_USER_STATUS: FAILED")
		print (" ")
		time.sleep(3)

#Part 2C: Details of password change
linecounterC = -1
for line in fdata:
	line = line.strip()
	linecounterC += 1
	if "/usr/bin/passwd" in line:
		if linecounterC+1 <= len(fdata):
			if "by (" in fdata[linecounterC+1]:
				exeuserC = re.search("(?<=by\s\()(.*?)(?=\))", fdata[linecounterC+1])
			else:
				exeuserC = re.search("(?<=sudo:\s)(.*?)(?=\s:)", line)
		changepwC = re.search("(?<=passwd\s)(.*)", line)
		dateC = re.search("[0-9]{1,4}-[0-9]{1,2}-[0-9]{1,2}", line)
		timeC = re.search("[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}", line)
		print("EVENT TYPE: change_password")
		if exeuserC.group() == "uid=1000":
			print("EXECUTION_USERNAME: kali")
		elif  exeuserC.group() == "uid=0":
			print("EXECUTION_USERNAME: root")
		else:
			print(f"EXECUTION_USERNAME: {exeuserC.group()}")
		print(f"USER_OF_PASSWORD: {changepwC.group()}")
		print(f"TIMESTAMP: {dateC.group()} {timeC.group()}")
		if linecounterC+3 <= len(fdata):
			if "passwd[" in fdata[linecounterC+3] and "couldn't" in fdata[linecounterC+3]:
				print ("PASSWORD_CHANGE_STATUS: FAILED")	
		print (" ")	
		time.sleep(3)

#Part 2D: Details of su command usage
linecounterD = -1
for line in fdata:
	line = line.strip()
	linecounterD += 1
	if "/usr/bin/su" in line:
		if linecounterD+1 <= len(fdata):
			if "by (" in fdata[linecounterD+1]:
				exeuserD = re.search("(?<=by\s\()(.*?)(?=\))", fdata[linecounterD+1])
			else:
				exeuserD = re.search("(?<=sudo:\s)(.*?)(?=\s:)", line)
		dateD = re.search("[0-9]{1,4}-[0-9]{1,2}-[0-9]{1,2}", line)
		timeD = re.search("[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}", line)
		print("EVENT TYPE: su_command")
		if exeuserD.group() == "uid=1000":
			print("EXECUTION_USERNAME: kali")
		elif  exeuserD.group() == "uid=0":
			print("EXECUTION_USERNAME: root")
		else:
			print(f"EXECUTION_USERNAME: {exeuserD.group()}")
		print(f"TIMESTAMP: {dateD.group()} {timeD.group()}")
		if "user NOT in sudoers" in line:
			print ("SU_COMMAND_STATUS: FAILED")
		print (" ")
		time.sleep(3)

#Part 2E: Details of sudo usage
linecounterE = -1
for line in fdata:
	line = line.strip()
	linecounterE += 1
	if "sudo:" and "COMMAND=" in line:
		if linecounterE+1 <= len(fdata):
			if "by (" in fdata[linecounterE+1]:
				exeuserE = re.search("(?<=by\s\()(.*?)(?=\))", fdata[linecounterE+1])
			else:
				exeuserE = re.search("(?<=sudo:\s)(.*?)(?=\s:)", line)
		dateE = re.search("[0-9]{1,4}-[0-9]{1,2}-[0-9]{1,2}", line)
		timeE = re.search("[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}", line)
		print("EVENT TYPE: sudo_usage")
		if exeuserE.group() == "uid=1000":
			print("EXECUTION_USERNAME: kali")
		elif exeuserE.group() == "uid=0":
			print("EXECUTION_USERNAME: root")
		else:
			print(f"EXECUTION_USERNAME: {exeuserE.group()}")
		if linecounterE+1 <= len(fdata):
			if "/usr/bin" in line and "by (" in fdata[linecounterE+1]:
				cmdtypeE = re.search("(?<=/usr/bin/)(.*)", line)
				print(f"COMMAND_EXECUTED: {cmdtypeE.group()}")
			elif "/usr/sbin" in line and "by (" in fdata[linecounterE+1]:
				cmdtypeE = re.search("(?<=/usr/sbin/)(.*)", line)
				print(f"COMMAND_EXECUTED: {cmdtypeE.group()}")
			else:
				if "/usr/bin" in line:
					cmdfailedE = re.search("(?<=/usr/bin/)(.*)", line)
				elif "/usr/sbin" in line:
					cmdfailedE = re.search("(?<=/usr/sbin/)(.*)", line)
				else:
					cmdfailedE = re.search("(?<=COMMAND=)(.*)", line)
				print(f"COMMAND_EXECUTED: {cmdfailedE.group()}")
		print(f"TIMESTAMP: {dateE.group()} {timeE.group()}")
		print (" ")
		time.sleep(3)

#Part 2F: Details of failed sudo usage
for line in fdata:
	line = line.strip()
	if "sudo:" and "COMMAND=" in line:
		dateF = re.search("[0-9]{1,4}-[0-9]{1,2}-[0-9]{1,2}", line)
		timeF = re.search("[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}", line)
		exeuserF = re.search("(?<=sudo:\s)(.*?)(?=\s:)", line)
		if "/usr/bin" and "user NOT in sudoers" in line:
			cmdfailedF = re.search("(?<=COMMAND=/usr/bin/)(.*)", line)
			print("ALERT!")
			print("EVENT TYPE: sudo_failed")
			print(f"EXECUTION_USERNAME: {exeuserF.group()}")
			print(f"COMMAND_EXECUTED: {cmdfailedF.group()}")
			print(f"TIMESTAMP: {dateF.group()} {timeF.group()}")
			print (" ")
			time.sleep(3)
		elif "/usr/sbin" and "user NOT in sudoers" in line:
			cmdfailedF = re.search("(?<=COMMAND=/usr/sbin/)(.*)", line)
			print("ALERT!")
			print("EVENT TYPE: sudo_failed")
			print(f"EXECUTION_USERNAME: {exeuserF.group()}")
			print(f"COMMAND_EXECUTED: {cmdfailedF.group()}")
			print(f"TIMESTAMP: {dateF.group()} {timeF.group()}")
			print (" ")
			time.sleep(3)
		elif "command not allowed" in line:
			cmdfailedF = re.search("(?<=COMMAND=)(.*)", line)
			print("ALERT!")
			print("EVENT TYPE: sudo_failed")
			print(f"EXECUTION_USERNAME: {exeuserF.group()}")
			print(f"COMMAND_EXECUTED: {cmdfailedF.group()}")
			print(f"TIMESTAMP: {dateF.group()} {timeF.group()}")
			print (" ")
			time.sleep(3)
