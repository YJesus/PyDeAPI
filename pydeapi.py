import os
import re
import subprocess

for processPid in os.listdir("/proc"):
	
	maps = '/proc/'+processPid+'/maps'
	
	if os.path.exists(maps) : 
		
		file = open(maps, "r")

		for libs in file.readlines():
			
			match = re.search(r'\s[\w-][\w-]([\w-])[\w-].*\s\s\s\s*([\w\/].*)' , libs)
			
			if  match and match.group(1) == 'x':
	
				isdeleted = re.search(r'\(deleted\)' , match.group(2))
				
				if not isdeleted:
				
					command = 'rpm -Vf "'+match.group(2)+'"' 
					
					process = subprocess.Popen([command], stdout=subprocess.PIPE,shell=True)
					output = process.communicate()[0]
					
					if output :
						
						thisfile = re.search(match.group(2) , output)
						
						if thisfile:
							print "Suspicious lib %s in PID %s" % (match.group(2), processPid)
				
