#!/usr/bin/python3

#
# retrieve last message from TD sensor platform 
#
# code under GPLv2

# some libs
import urllib.request
import urllib.parse
import json

# some private const (no push to public repo)
import private
TD12XX_ID  = private.TD12XX_ID
TD12XX_KEY = private.TD12XX_KEY

# get token
token_params = urllib.parse.urlencode({'sn': TD12XX_ID, 'key': TD12XX_KEY})
f = urllib.request.urlopen("http://sensor.insgroup.fr/iot/devices/crc.json?%s" % token_params)
token = f.read().decode('utf-8')

# get messages history (last 3)
msg_params = urllib.parse.urlencode({'sn': TD12XX_ID, 'amount': 3})
req = urllib.request.Request("https://sensor.insgroup.fr/iot/devices/msgs/history.json?%s" % msg_params)
req.add_header('X-Snsr-Device-Key', token)
f = urllib.request.urlopen(req)
msg_json = f.read().decode('utf-8')
msgs = json.loads(msg_json)
for msg in msgs:
  print(msg)
  print("\n")

