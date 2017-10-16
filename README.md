# Android-Mitm-Proxy
A python script that analyses android applications and logs their connections through a Mitm-proxy.
Every apk within a previously chosen folder will be installed, launched and uninstalled one after the other.
During this process a separate proxy server logs every connection made from those apps.



## Structure

Genymotion is used for emulating the Android OS, because a transpiler from ARM to x86 is available.
This enables genymotion to run either ARM or x86 apps and therefore offers more flexibility.

Note:

	- auto-allow super-user access
	- [Errno 32] Brocken pipe
		this is a know bug in the ServerSocket python library
		and can only be resolved, if the library code is modified
		https://bugs.python.org/issue14574



## How to setup

Unfortunately it is impossible to let genymotion run in a virtual machine. Therefore 
everythin has to be done on a physical machine.
Most of the steps for setting up the environment should be OS-independent though.

- download and install virtualbox
	- https://www.virtualbox.org/wiki/Downloads

- download and install of genymotion:
	- genymotion.com/download
	- dummy credentials:
		- username: bugmenot123456789, password: bugmenot
	- detailed instructions for windows, linux and MacOS can be found here:
		https://docs.genymotion.com/pdf/PDF_User_Guide/Genymotion-2.10.0-User-Guide.pdf

- go ahead and set up a virtual android device
	- the device used during development was a Nexus-5X with Android 7.1 (API 25)




