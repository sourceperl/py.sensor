#!/usr/bin/python3

#
# test script for sensor module
#
# code under GPLv2

# some libs
import sensor
import time

# some private const (no push to public repo)
import private
TD12XX_ID  = private.TD12XX_ID
TD12XX_KEY = private.TD12XX_KEY

# use sensor object
sensor = sensor.Sensor()
# get token
if (not sensor.set_device(TD12XX_ID, TD12XX_KEY)):
  print('get token ko !')
  exit(1)

# get message history
msgs = sensor.get_history(20)
# skip if error
if msgs == 0:
  exit(2)

# prind header
print('{0:16s}  {1:15s}  {2:20s}  {3:4s}  {4:2s}'.format('date-time', 'msg-type', 'payload', 'stat', 'lv'))

for msg in msgs:
  # test and format vars from JSON
  try:
    msg_when = msg['when']/1000
  except:
    msg_when = 0;
  try:
    msg_type = msg['type']
  except:
    msg_type = 'unknown'
  try:
    msg_station = msg['station']
  except:
    msg_station = 'null'
  try:
    msg_lvl = round(float(msg['lvl']))
  except:
    msg_lvl = 'null'
  try:
    msg_pay = msg['payload']
  except:
    msg_pay = ''
  # print history
  print('{0:16s}  {1:15s}  {2:20s}  {3:4s}  {4:02d}'.format(time.strftime("%d/%m/%Y %H:%M", time.localtime(int(msg_when))),
                                                            msg_type, msg_pay, msg_station, msg_lvl))

