#! /usr/bin/python
# coding: utf-8


from sys import argv
import os
import time
import csv
from miproxy.proxy import MitmProxy, ProxyHandler


connectionList = ['packageName', 'connections']
logPath = 'Out/Logs/monkeyMitmProxyLogs'
fileName = './' + logPath + '/loggedConnections_' + \
    time.asctime(time.localtime(time.time()))


class MitmProxyHandler(ProxyHandler):

    def mitm_request(self, data):
        # print '>> %s' % repr(data[:100])
        # possibility to modify outgoing request
        return data

    def mitm_response(self, data):
        # print '<< %s' % repr(data[:100])
        # possibility to modify incoming response
        return data

    def log_message(self, format, *args):

        global connectionList
        global fileName

        headers = ('get', 'post', 'connect')

        potentialAddress = str(args[0])

        if potentialAddress.lower().startswith(headers):
            print potentialAddress
            if 'CUSTOM-LOGGING' in potentialAddress:
                connectionList = []
                # extract android package name from custom url
                # syntax:    http://CUSTOM-LOGGING.com/" + packageName
                connectionList.append(
                    potentialAddress.split(' ')[1].split('/')[-1])

            elif 'END-LOGGING' in potentialAddress:
                # append list of logged connections to logfile
                with open(fileName + '.csv', 'ab+') as csvfile:
                    logwriter = csv.writer(
                        csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    logwriter.writerow(connectionList)
            else:
                # append connection to list of logged connections
                connectionList.append(potentialAddress)


if __name__ == '__main__':
    proxy = None

    # create subdirectoy for evaluation data
    if not os.path.exists(logPath):
        os.makedirs(logPath)

    if not argv[1:]:
        proxy = MitmProxy(RequestHandlerClass=MitmProxyHandler)
    else:
        proxy = MitmProxy(
            RequestHandlerClass=MitmProxyHandler, ca_file=argv[1])
    try:

        # initalize log file
        with open(fileName + '.csv', 'wb+') as csvfile:
            logwriter = csv.writer(
                csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            logwriter.writerow(connectionList)

        proxy.serve_forever()

    except KeyboardInterrupt:
        proxy.server_close()
