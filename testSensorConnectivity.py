import Adafruit_DHT as dht
from time import sleep

#This tests to make sure the sensor is accessible and returning data. Every 5 seconds. 
while True:
    h,t = dht.read_retry(dht.DHT22, 4)
    f = format((9.0/5.0 * t + 32), '.1f')
    print h,t,f
    sleep(5)
