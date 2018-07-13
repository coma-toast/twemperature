
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

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

#Open config file
f = open(os.path.join(__location__, 'configFile.json'));
configFile = json.load(f)
print configFile
pprint(configFile)


#Twitter API keys
CONSUMER_KEY = configFile["CONSUMER_KEY"]
CONSUMER_SECRET = configFile["CONSUMER_SECRET"]
ACCESS_KEY = configFile["ACCESS_KEY"]
ACCESS_SECRET = configFile["ACCESS_SECRET"]

pprint (CONSUMER_KEY)
pprint(CONSUMER_SECRET)
pprint(ACCESS_KEY)
pprint(ACCESS_SECRET)

#Test Twitter auth
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#Send a startup tweet. Timezone is only UTC for now.
now = datetime.datetime.now()
api.update_status('Up and running. ' + now.strftime("%Y-%m-%d %H:%M:%S") + ' #twemperature')

#Set the limit to what you want, in Celcius
#32f = 0c; 30f = -1.1c; 80f = 26.6c; 72f = 22.2c; 14f = -10c

# while True:
# 	h,t = dht.read_retry(dht.DHT22, 4)
# 	f = format((9.0/5.0 * t + 32), '.1f')
# 	h = format(h, '.1f')
# 	print h
# 	print t
# 	print 'Fahrenheit={0:0.1f}'.format(9.0/5.0 * t + 32) + ' Humidity= ' + str(h)
# 	if t > -9:
# 		print 'too hot!'
# 		#api.update_status(' High Temperature: ' + str(f) + 'F Humidity: ' + str(h) + '% ' + '#twemperature')
# 		print 'High Temperature: ' + str(f) + 'F Humidity: ' + str(h) + '%'
# 		sleep(5)
# 	else:
# 		print 'normal'
# 		sleep(5)
f.close()
