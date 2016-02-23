# PyDeAPI
Python script to detect API hooking in Linux 

PyDeAPI  searches loaded libs in /proc/pid/maps and tries to find them in rpm DB to discover non installed or
modified libs 

Currently it only works in RPM linux distros (CentOS, Fedora, etc)
