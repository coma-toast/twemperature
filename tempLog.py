
# -*- coding: utf-8 -*-
import sys
import os as os
from time import sleep
import tweepy
from decimal import Decimal
import Adafruit_DHT as dht
import datetime
import json
from pprint import pprint
import argparse
import logging

#arg parser. It parses args.
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
#parser.add_argument("-c", "--celcius", help="use celcius", action="store_true", default=False)
parser.add_argument("-f", "--fahrenheit", help="use Fahrenheit", action="store_false")
parser.add_argument("-H", "--high", help="monitor for a high temperature (C)", action="store", type=int)
parser.add_argument("-L", "--low", help="monitor for a low temperature (C)", action="store", type=int)
parser.add_argument("-i", "--interval", help="set polling interval when a high/low condition is met", action="store", type=int, default=60)
parser.add_argument("--logfile", help="Path to the logfile. If empty, output is STDOUT/STDERR")

args = parser.parse_args()
if args.verbose:
    print "verbosity turned on"

#Set some logging options
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
log_to_console = logging.StreamHandler()
log_to_console.setLevel(logging.ERROR)

#Setup --logfile options
try:
    if args.logfile:
        log_to_file = logging.FileHandler(args.logfile)
        log_to_file.setLevel(logging.DEBUG)
        logger.addHandler(log_to_file)
        if args.verbose:
            logger.info("Verbose logging enabled")
    else:
        logger.addHandler(log_to_console)
        if args.verbose:
            logger.info("Verbose logging enabled")
except IOError as e:
    # logger.critical("Error trying to open {} error({}): {}".format(args.logfile, e.errno, e.strerror))
    logger.critical("Error")



#set __location__ to current working path
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

#Open config file
f = open(os.path.join(__location__, 'configFile.json'));
configFile = json.load(f)
#print configFile
# pprint(configFile)



#Twitter API keys
CONSUMER_KEY = configFile["CONSUMER_KEY"]
CONSUMER_SECRET = configFile["CONSUMER_SECRET"]
ACCESS_KEY = configFile["ACCESS_KEY"]
ACCESS_SECRET = configFile["ACCESS_SECRET"]


#Test Twitter auth
def testAuth():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    if args.verbose:
        pprint(auth)
        pprint(api)
        logger.info(api, auth)
    checkin(api)
    pollTemp(api, args.interval, args.low, args.high)



#Send a startup tweet. Timezone is only UTC for now.
def checkin(api):
    now = datetime.datetime.now()
    api.update_status('Up and running. ' + now.strftime("%Y-%m-%d %H:%M:%S") + ' #twemperature')
    print ("Checked in at " + str(now))
    if args.verbose: logger.info("Checked in at " + str(now))

#Set the limit to what you want, in Celcius
#32f = 0c; 30f = -1.1c; 80f = 26.6c; 72f = 22.2c; 14f = -10c

def pollTemp(api, i, min, max):
    print("pollTemp")
    while True:
    	h,t = dht.read_retry(dht.DHT22, 4)
    	f = format((9.0/5.0 * t + 32), '.1f')
    	h = format(h, '.1f')
        if args.high:
            if checkHigh(t, max):
                if args.fahrenheit:
                    print 'High Temperature: ' + str(f) + 'F Humidity: ' + str(h) + '%'
                    api.update_status(' High Temperature: ' + str(f) + 'F Humidity: ' + str(h) + '% ' + '#twemperature')
                if args.celcius:
                    print 'High Temperature: ' + str(t) + 'C Humidity: ' + str(h) + '%'
                    api.update_status(' High Temperature: ' + str(t) + 'C Humidity: ' + str(h) + '% ' + '#twemperature')
                sleep(i)
            else:
                sleep(i)
        if args.low:
            if checkLow(t, min):
                if args.fahrenheit: print 'Low Temperature: ' + str(f) + 'F Humidity: ' + str(h) + '%'
                if args.celcius: print 'Low Temperature: ' + str(t) + 'C Humidity: ' + str(h) + '%'
                sleep(i)
            else:
                sleep(i)
        else:
            sleep(i)

        # if args.fahrenheit:
        #     print h,f,t
        #     if args.verbose:
        #         print 'Fahrenheit={0:0.1f}'.format(9.0/5.0 * t + 32) + ' Humidity= ' + str(h)
        #         print 'Celcius={0:0.1f}'.format(t) + ' Humidity= ' + str(h)
        #     if args.high:
        #         if checkHigh(t, max):
        #             print 'High Temperature: ' + str(f) + 'F Humidity: ' + str(h) + '%'
        #             sleep(i)
        #         else:
        #             sleep(i)
        #     sleep(i)
        # elif args.celcius:
        #     print h,f,t
        #     if args.verbose:
        #         print 'Fahrenheit={0:0.1f}'.format(9.0/5.0 * t + 32) + ' Humidity= ' + str(h)
        #         print 'Celcius={0:0.1f}'.format(t) + ' Humidity= ' + str(h)
        #     if args.high:
        #         if checkHigh(t, max):
        #             print 'High Temperature: ' + str(t) + 'F Humidity: ' + str(h) + '%'
        #             sleep(i)
        #         else:
        #             sleep(i)
        #     sleep(i)

    	# if t > -9:
    	# 	print 'too hot!'
    	# 	#api.update_status(' High Temperature: ' + str(f) + 'F Humidity: ' + str(h) + '% ' + '#twemperature')
    	# 	print 'High Temperature: ' + str(f) + 'F Humidity: ' + str(h) + '%'
        #
    	# else:
        #     if args.verbose:
        #         print 'normal temp'
    	# 	sleep(interval)

def checkHigh(temp, max):
    if temp >= max:
        if args.verbose:
            print 'Temperature exceeded threshold'
            print 'High Temperature: ' + str(f) + 'F Humidity: ' + str(h) + '%'
            logger.info('High Temperature: ' + str(f) + 'F Humidity: ' + str(h) + '%')
            return True
        else:
            return False

def checkLow(temp, min):
    if temp <= min:
        if args.verbose:
            print 'Temperature exceeded threshold'
            print 'Low Temperature: ' + str(f) + 'F Humidity: ' + str(h) + '%'
            logger.info('Low Temperature: ' + str(f) + 'F Humidity: ' + str(h) + '%')
            return True
        else:
            return False

f.close()

testAuth()
