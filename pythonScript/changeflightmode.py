import sys
from pymavlink import mavutil

master = mavutil.mavlink_connection('udpin:127.0.0.1:14550')
master.wait_heartbeat()

mode1 = 'GUIDED'
mode2 = 'LAND'

mode_id = master.mode_mapping()[mode]

master.mav.set_mode_send(
  master.target_system,
  mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
  mode_id)

while True:
  ack_msg = master.recv_match(type='COMMAND_ACK', blocking=True)

