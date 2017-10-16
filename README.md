# Android-Mitm-Proxy
A python script that analyzes android applications and logs their connections through a Mitm-proxy.
Every apk within a previously chosen folder will be installed, launched and uninstalled one after the other.
During this process a separate proxy server logs every connection made from those apps.



## Structure

Genymotion is used for emulating the Android OS, because a transpiler from ARM to x86 is available.
This enables genymotion to run either ARM or x86 apps and therefore offers more flexibility.

This application consists of two main python scripts, the monkeyMitmProxy which is a modified version of the [mitmproxy](https://github.com/mitmproxy/mitmproxy), and the monkeyChaser which utilizes the [monkeyrunner](https://developer.android.com/studio/test/monkeyrunner/MonkeyRunner.html) tool to connect to an android emulator instance.

To run this project first launch the monkeyMitmProxy.py, which then runs passively in the background, logs all connections and saves them to a csv file. Afterwards the monkeyChaser.py can be launched as the main tool. The mymonkey.py script will handle the actual connection and app life cycle during the procedure and is called by the monkeyChaser inherently when needed.


## Setup

Unfortunately it is impossible to let genymotion run in a virtual machine. Therefore everything has to be done on a physical machine.
Most of the steps for setting up the environment should be OS-independent.

- Download and install virtualbox
	- https://www.virtualbox.org/wiki/Downloads
	- genymotion depends on virtual machine in the background

- Download and install genymotion:
	- https://www.genymotion.com/download/
	- dummy credentials for login:
		- username: bugmenot123456789, password: bugmenot
	- detailed instructions for windows, linux and MacOS can be found here:
		https://docs.genymotion.com/pdf/PDF_User_Guide/Genymotion-2.10.0-User-Guide.pdf

- Go ahead and set up a virtual android device
	- the device used during development was a Nexus-5X with Android 7.1 (API 25)

- To route the android traffic through the mitm proxy, please set the correct addresses.
 The android emulator by default creates a NAT network with the physical machine as router. This address, in my case 192.168.58.1:8080, needs to be entered as proxy server for android. To enter a proxy inside the Android OS, please follow these steps:

	- Go to Settings
	- Click on Wi-Fi
	- Long-click on WiredSSID
	- Click on Modify network
	- Set Proxy to manual and type the "proxy" and "port"



### Notes

	- auto-allow super-user access
		- this might be a good idea, if apps requiring root privileges are tested
	- [Errno 32] Brocken pipe
		- this is a know bug in the ServerSocket python library
		and can only be resolved, if the library code is modified
		https://bugs.python.org/issue14574

