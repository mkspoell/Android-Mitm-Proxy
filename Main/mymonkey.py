#! /usr/bin/env monkeyrunner
# coding: utf-8


from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

from subprocess import Popen, PIPE
import commands
import sys, os
import time


def main():

	if len(sys.argv) == 5:
		runMonkeyScript(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
	else:
		print "Argument missing!\n Usage: >> monkeyrunner mymonkey.py <filename> <package-name> <mainActivity> <intervall>"


def runMonkeyScript(fileName, packageName, mainActivity, intervall):
	# starting script
	print "starting monkey script"

	# connection to the current device, and return a MonkeyDevice object
	device = MonkeyRunner.waitForConnection()

	# check if apk is already installed and install, if not
	apk_path = device.shell('pm path '+ packageName)
	if apk_path.startswith('package:'):
	    print packageName + " already installed."
	else:
	    print packageName + " is not installed, installing " + fileName + " ..."
	    if not (os.path.isfile('myApps/' + fileName)):
	    	print "Package file not found"
	    	return
	    device.installPackage('myApps/' + fileName)

   # launching the app
	print "launching " + mainActivity + "..."
	device.startActivity(component= packageName + '/' + mainActivity) #apk + '/' + apk + '.MainActivity')

	# intervall to catch network traffic
	time.sleep(int(intervall))

	# simulate keypress 'HOME' and uninstall apk
	device.press('KEYCODE_HOME', MonkeyDevice.DOWN_AND_UP)
	print "returned 'HOME'"
	device.removePackage(packageName)
	print "uninstalled apk"

	print "end of script\n"



if __name__ == '__main__':
	main()



























