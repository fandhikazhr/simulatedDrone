from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('connect', default='127.0.0.1:14550')
args = parser.parse_args()

print('Connected to vehicle on: %s' % args.connect)
vehicle = connect(args.connect, baud=57600, wait_ready=True)

def arm_and_takeoff(aTargetAltitude):
  print "Basic pre-arm checks"
  while not vehicle.is_armable:
    print('Waiting for vehicle to initialise ...')
    time.sleep(1)
    
  print('Arming motors')
  vehicle.mode = VehicleMode("GUIDED")
  vehicle.armed = True
  
  while not vehicle.armed:
    print('Waiting for arming motors ...')
    time.sleep(5)
    
