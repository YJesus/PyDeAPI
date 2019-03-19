# PyDeAPI
Python script to detect API hooking in Linux 

PyDeAPI  searches loaded libs in /proc/pid/maps and tries to find them in rpm or dpkg DB to discover non installed or
modified libs 

Currently it works in RPM and DPKG linux distros (CentOS, Fedora, Debian, Ubuntu)
