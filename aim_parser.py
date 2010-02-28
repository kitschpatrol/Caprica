# Converts my aim logs to our special format
# CHATID,DATE,AUTHOR,CHAT
import re
import time
			
file = open("../aim.txt")
aim_log = file.readlines(10000)



#Session Start (obrigado:sandieganVTEC): Tue Mar 30 16:26:09 2004
#Session Close (sandieganVTEC): Tue Mar 30 16:22:16 2004

#End of ollHONDAllo buffer: Sat Sep 29 02:07:00 2001
#------------------------------------------------
#Start of ollHONDAllo buffer: Sat Sep 29 02:14:02 2001


chat_id = 0
unix_time= 0.0

#find the conversation bounds
for line in aim_log:
	# Remove endline and white space
	line = line.strip()

	# Make sure it's a reasonable line and not meta-cruft	
	if len(line) > 0 and not re.match("^\*", line) and not re.match("^-", line):
		# Look for conversation start
		if re.match("^Start of", line) or re.match("^Session Start", line):
			chat_id += 1;
			# extract the date
			# comes in as Sep 29 02:14:02 2001	
			time_string = line[len(line) - 20:len(line)]
			python_time = time.strptime(time_string,"%b %d %H:%M:%S %Y")
			unix_time = time.mktime(python_time)
			
		else:
			
		
			print str(chat_id) + "," + str(unix_time) + "," + "author" + "," + line


		#if re.match("^End of", line) or re.match("^Session Close", line):
			# Do something at session end, if we want
			