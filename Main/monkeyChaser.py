#! /usr/bin/python
# coding: utf-8


from subprocess import Popen, PIPE
import os, io, sys
import time
import json #simplejson as json
# import urllib2
import requests


class monkeyChaser():

	def __init__(self):

		self.apps = []
		self.proxy={'http' : 'http://192.168.43.220:8080'}

		self.pathToAppFolder = './myApps/'
		self.monkeyScriptLoggingPath = 'Out/Logs/monkeyChaserLogs'
		self.dataBasePath = 'Out/database'

		self.logFileName = './' + self.monkeyScriptLoggingPath + '/script-'+ time.asctime( time.localtime(time.time())) + '.log'

		# create subdirectoy for evaluation data
		if not os.path.exists(self.dataBasePath):
		    os.makedirs(self.dataBasePath)

		if not os.path.exists(self.monkeyScriptLoggingPath):
		    os.makedirs(self.monkeyScriptLoggingPath)

	def main(self):


		while True:
			try:
				self.clrScreen()
				print '\n\n  MENU : '
				print '----------------------------'

				print '\n 1 : Read apk details from app folder'
				print '\n 2 : Import apk details from json file'
				print '\n 3 : Let monkeyrunner analyse the apks'

				print '\n 0 : Exit'
				inpt = raw_input('\nInput: ')
				self.clrScreen()


				if (inpt == '1') : self.readAppFolder()
				elif (inpt == '2') : self.importApkDetailJson()
				elif (inpt == '3') : self.chaseTheMonkeyHorde()

				elif (inpt == '0') :
					break
				else:
					print '\n\n\tGiven number is not a valid choice. Please try again ...'

				raw_input('\n\n\n\nHit \'Enter\' to go back to menu!')
			except:
				print 'Error occured...'
				break



		
		# self.readAppFolder(self.pathToAppFolder)

		# letTheMonkeyRun('Firefox-Focus-privacy-browser_1.3_apk-dl.com.apk', 'org.mozilla.focus', 'org.mozilla.focus.activity.MainActivity')

		# self.chaseTheMonkeyHorde()




	"""
		Analyzing the files in a given folder.
		The 'aapt' command is issued on each file to determine
		the android package name and the name of the launchable
		activity. The data is saved to a json file.

	"""
	def readAppFolder(self):
		inpt = raw_input('\nPath to app folder (default: "./myApps"): ')

		path = inpt if os.path.exists(inpt) else self.pathToAppFolder 

		for file in os.listdir(path):
			if str(file).endswith('.apk'):
				sysCall = Popen(['aapt', 'dump', 'badging', path + file], stdout=PIPE, stderr=PIPE, stdin=PIPE)
				aaptDump = sysCall.stdout.readlines()

				jsonObj = {} 
				jsonObj['file-name'] = file
				for line in aaptDump:
					if line.startswith('package: name='):
						jsonObj['package-name'] =  line.split('\'')[1]
					elif line.startswith('launchable-activity: name='):
						jsonObj['main-activity'] =  line.split('\'')[1]

				self.apps.append(jsonObj)
				# package: name='com.zimperium.zanti'
				# launchable-activity: name='com.zimperium.zanti.zcloud.ZcloudMainActivity'


		self.clrScreen()
		print '\n Your apks have been analysed.\n The results are also saved into a json file for further usage in "/Out/database".\n\n'
		print self.jsonPrettyPrint(self.apps)
		with open(self.dataBasePath + '/appDetails.json', 'w') as file:
			json.dump(self.apps, file)


	def importApkDetailJson(self):
		if os.path.exists(self.dataBasePath + '/appDetails.json'):
			with open(self.dataBasePath + '/appDetails.json', 'r') as jsonFile:
				self.apps = json.load(jsonFile)
			self.clrScreen()
			print '\n The following apks have been read.\n\n'
			print self.jsonPrettyPrint(self.apps)
		else:
			print 'Unfortunately there is no existing json database.'


	def chaseTheMonkeyHorde(self):
		if len(self.apps) == 0:
			print 'Unfortunately there are no apk data loaded.\nPlease import a json file or analyse an apk folder first.'
			return 

		for app in self.apps:
			self.letTheMonkeyRun(app['file-name'], app['package-name'], app['main-activity'])


	def letTheMonkeyRun(self, filename, packageName, mainActivity):
		print 'launching the Monkey...'

		# urllib2.urlopen("http://LOG.com/" + packageName).read()
		session = requests.Session()
		r = session.get('http://CUSTOM-LOGGING.com/' + packageName, proxies=self.proxy)

		# modified version of the proposed solution from https://stackoverflow.com/questions/18421757/live-output-from-subprocess-command
		# self.logFileName = './logs/script-'+ time.asctime( time.localtime(time.time())) + '.log'
		with io.open(self.logFileName, 'ab') as writer, io.open(self.logFileName, 'rb', 1) as reader:
			process = Popen(['monkeyrunner', 'mymonkey.py', filename, packageName, mainActivity], stdout=writer, stderr=PIPE, stdin=PIPE)
			# process = subprocess.Popen(command, stdout=writer)
			while process.poll() is None:
				sys.stdout.write(reader.read())
				time.sleep(0.5)
			# Read the remaining
			sys.stdout.write(reader.read())

		r = session.get('http://END-LOGGING.com/' + packageName, proxies=self.proxy)

		# sysCall = Popen(['monkeyrunner', 'mymonkey.py', filename, packageName, mainActivity], stdout=PIPE, stderr=PIPE, stdin=PIPE)
		# monkeyDump = sysCall.stdout.read()
		# print monkeyDump


	def jsonPrettyPrint(self, json_object):
	    return json.dumps(json_object, sort_keys=True, indent=4, separators=(',', ': '))

	def clrScreen(self):	
		sys.stderr.write("\x1b[2J\x1b[H")





if __name__ == '__main__':
	monkeyChaser = monkeyChaser()
	monkeyChaser.main()
