#! /usr/bin/env monkeyrunner
# coding: utf-8


from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
# from monkeyrunner import MonkeyRunner, MonkeyDevice
from subprocess import Popen, PIPE
import commands
import sys, os
import time
# import json #simplejson as json


evaluationPath = 'Out/evaluation'

def main():

	# create subdirectoy for evaluation data
	if not os.path.exists(evaluationPath):
	    os.makedirs(evaluationPath)

	# pathToAppFolder = '/Volumes/Data/University/UniMarburg/10.Semester/FoPra_MITM/Main/myApps'
	# readAppFolder('./myApps/')

	if len(sys.argv) == 4:
		runMonkeyScript(sys.argv[1], sys.argv[2], sys.argv[3])
	else:
		print "Argument missing!\n Usage: >> monkeyrunner mymonkey.py <filename> <package-name> <mainActivity>"
	#runMonkeyScript('com.spotify.music')


def runMonkeyScript(fileName, packageName, mainActivity):
	# starting script
	print "starting monkey script"

	

	# connection to the current device, and return a MonkeyDevice object
	device = MonkeyRunner.waitForConnection()

	apk_path = device.shell('pm path '+ packageName)
	if apk_path.startswith('package:'):
	    print packageName + " already installed."
	else:
	    print packageName + " is not installed, installing " + fileName + " ..."
	    if not (os.path.isfile('myApps/' + fileName)):
	    	print "Package file not found"
	    	return
	    device.installPackage('myApps/' + fileName)

	print "launching " + mainActivity + "..."
	device.startActivity(component= packageName + '/' + mainActivity) #apk + '/' + apk + '.MainActivity')

	# TODO: catch network traffic
	MonkeyRunner.sleep(4)

	# safe screenshot to subdirectory
	directory = evaluationPath + '/' + packageName
	if not os.path.exists(directory):
	    os.makedirs(directory)

	filename = packageName + ' - ' + time.asctime( time.localtime(time.time()) )
	result = device.takeSnapshot()
	result.writeToFile(directory + '/'+ filename + '.png','png')
	print "screen 1 taken"

	device.press('KEYCODE_HOME', MonkeyDevice.DOWN_AND_UP)
	print "returned 'HOME'"
	device.removePackage(packageName)
	print "uninstalled apk"

	print "end of script"



if __name__ == '__main__':
	main()



























