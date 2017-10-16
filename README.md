# Android-Mitm-Proxy
A python program that analyses android applications and logs their connections through a Mitm-proxy



## Struktur

Als Emulator wird Genymotion verwendet, da hierfür einen transpiler von ARM auf x86 zur Verfügung steht.


Note:

	- auto-allow super-user access
	- [Errno 32] Brocken pipe
		this is a know bug in the ServerSocket python library
		and can only be resolved, if the library code is modified
		https://bugs.python.org/issue14574



## How to setup

- install a virtual machine if you prefer to run everything from within a VM
- further instructions will assume you are working within a debian virtual machine
	- specifically tested was a Ubuntu-16.04 VM

- download and install genymotion from genymotion.com/download
	- dummy credetials: username: bugmenot123456789, password: bugmenot
	- follow their install instructions on
		https://docs.genymotion.com/pdf/PDF_User_Guide/Genymotion-2.10.0-User-Guide.pdf

- go ahead and set up a virtual android device
	- the device used during development was a Nexus-5X with API 25




