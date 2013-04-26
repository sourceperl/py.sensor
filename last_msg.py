#!/usr/bin/python3

#
# retrieve last message from TD sensor platform 
#
# code under GPLv2

# some libs
import urllib.request
import urllib.parse
import json
import time

# some private const (no push to public repo)
import private
TD12XX_ID  = private.TD12XX_ID
TD12XX_KEY = private.TD12XX_KEY

# get token
token_params = urllib.parse.urlencode({'sn': TD12XX_ID, 'key': TD12XX_KEY})
try:
  f = urllib.request.urlopen("https://sensor.insgroup.fr/iot/devices/crc.json?%s" % token_params)
except:
  print('get_token: error, exit.')
  exit(1);
# read and check token
token    = f.read()
print("token (base64)  : %s" % token.decode('ascii'))

# get messages history in json format (last 3)
msg_params = urllib.parse.urlencode({'sn': TD12XX_ID, 'amount': 20})
try:
  req = urllib.request.Request("https://sensor.insgroup.fr/iot/devices/msgs/history.json?%s" % msg_params)
  req.add_header('X-Snsr-Device-Key', token)
  f = urllib.request.urlopen(req)
except:
  print('get_msg: error, exit.')
  exit(2)
msg_json = f.read()

# decode json
msgs = json.loads(msg_json.decode('ascii'))
for msg in msgs:
  # format json var
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
  # print history
  print('{0} {1:15s} {2} {3:02d}'.format(time.strftime("%d/%m/%Y %H:%M", time.localtime(int(msg_when))), msg_type, msg_station, msg_lvl))
