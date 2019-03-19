import os
import re
import subprocess

debian = '/etc/debian_version'
redhat = '/etc/redhat-release'

for processPid in os.listdir("/proc"):
	
	maps = '/proc/'+processPid+'/maps'
	
	if os.path.exists(maps) : 
		
		file = open(maps, "r")

		for libs in file.readlines():
			
			match = re.search(r'\s[\w-][\w-]([\w-])[\w-].*\s\s\s\s*([\w\/].*)' , libs)
			
			if  match and match.group(1) == 'x':
	
				isdeleted = re.search(r'\(deleted\)' , match.group(2))
				
				if not isdeleted:
					
					if os.path.exists(redhat) : 
						command = 'rpm -Vf "'+match.group(2)+'"' 
					
						processrpm = subprocess.Popen([command], stdout=subprocess.PIPE,shell=True)
						outputrpm = processrpm.communicate()[0]
					
						if outputrpm :
						
							thisfile = re.search(match.group(2) , outputrpm)
						
							if thisfile:
								print "Suspicious lib or process %s in PID %s" % (match.group(2), processPid)
								
					if os.path.exists(debian) :
						
						commandDPKG = 'dpkg -S "'+match.group(2)+'"'
						
						
						DEVNULL = open(os.devnull, 'wb')
						processdpkg = subprocess.Popen([commandDPKG], stdout=subprocess.PIPE,shell=True, stderr=DEVNULL)
						outputdpkg = processdpkg.communicate()[0]
						
						
						if processdpkg.returncode == 1:
							
							#dpkg is buggy to find package files 
							
							fixdpkgbug= re.sub('/usr',  '',    match.group(2))
							
							commandDPKG2 = 'dpkg -S "'+fixdpkgbug+'"'
						
							
							DEVNULL = open(os.devnull, 'wb')
							processdpkg2 = subprocess.Popen([commandDPKG2], stdout=subprocess.PIPE,shell=True, stderr=DEVNULL)
							outputdpkg2 = processdpkg2.communicate()[0]
							
							outputdpkg = outputdpkg2
							
							if processdpkg2.returncode == 1:
							
								print "Suspicious lib or process %s in PID %s" % (match.group(2), processPid)
						
							else:
								
								packagename = outputdpkg.split(":")
						
								commandDEBSUM = 'dpkg --verify "'+packagename[0]+'"'
						
							
								processdebsum = subprocess.Popen([commandDEBSUM], stdout=subprocess.PIPE,shell=True)
								outputdebsum = processdebsum.communicate()[0]
						
								if outputdebsum :
						
									thisfile = re.search(match.group(2) , outputdebsum)
						
									if thisfile:
										print "Suspicious lib or process %s in PID %s" % (match.group(2), processPid)
						
						
						
						
						
						
