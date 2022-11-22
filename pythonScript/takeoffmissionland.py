from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='127.0.0.1:14550')
args = parser.parse_args()

print('Connected to vehicle on: %s' % args.connect)
vehicle = connect(args.connect, baud=57600, wait_ready=True)

master = mavutil.mavlink_connection('udpin:127.0.0.1:14550')
master.wait_heartbeat()

# Choose Flight Mode
mode1 = 'GUIDED'

mode_id = master.mode_mapping()[mode1]

master.mav.set_mode_send(
  master.target_system,
  mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
  mode_id)

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
    
  print('Starting Takeoff !!!')
  vehicle.simple_takeoff(aTargetAltitude)
  
  while True:
    print("=> Altitude : ", vehicle.location.global_relative_frame.alt)
    if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
      print "Reached target altitude !!!"
      break
    time.sleep(1)

# start initial takeoff
arm_and_takeoff(10)
time.sleep(5)

print("Takeoff Successfully !!!")

# hovering 15 seconds
time.sleep(15)

# Mission Started
point1 = LocationGlobalRelative(-35.361354, 149.165218, 10)
vehicle.simple_goto(point1)
print("--> Going to Point 1")

time.sleep(5)

point2 = LocationGlobalRelative(-35.363244, 149.168801, 10)
vehicle.simple_goto(point2)
print("--> Going to Point 2")

time.sleep(5)
print("Mission Completed !!!")

# hovering 15 seconds
time.sleep(15)

# Change Flight Mode for Landing
mode2 = 'LAND'

mode_land = master.mode_mapping()[mode2]

master.mav.set_mode_send(
  master.target_system,
  mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
  mode_land)

print("Landing ...")

vehicle.close()
