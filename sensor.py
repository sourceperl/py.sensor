#!/usr/bin/python3

# 
# Python class for interface with Telecom Design Sensor platform
#
#
# code under GPLv2

# some libs
import urllib.request
import urllib.parse
import json

class Sensor:
  """
  Python module for interface with Telecom Design Sensor Web services

  usage sample:
    sensor = Sensor()
    sensor.set_device(your_id, your_key)
    msgs = sensor.get_last_msgs(30)
  """

  def __init__(self):
    """Class builder"""
    self.token         = ''
    self.device_id     = ''
    self.device_key    = ''
    self.lastHTTPError = 0
  
  def set_device(self, dev_id, dev_key):
    """
    Set device ID and Key
      return 1 if success
      return 0 if fail
    """
    self.device_id  = dev_id
    self.device_key = dev_key
    return self._update_token()

  def get_history(self, amount = 20, until = 0):
    """
    Get messages history in json format
      return an array of message if success
      return 0 if fail
    """
    params = {'sn': self.device_id, 'amount': amount}
    if (until > 0):
      params['until'] = until
    msg_params = urllib.parse.urlencode(params)
    try:
      req = urllib.request.Request("https://sensor.insgroup.fr/iot/devices/msgs/history.json?%s" % msg_params)
      req.add_header('X-Snsr-Device-Key', self.token)
      f = urllib.request.urlopen(req)
    except urllib.error.HTTPError as err:
      self.lastHTTPError = err.code
      return 0
    except:
      return 0
    msg_json = f.read()
    msgs = json.loads(msg_json.decode('ascii'))
    return msgs
  
  def _update_token(self):
    """
    Get the token for current device id/key
      return 1 if success
      return 0 if fail
    """
    token_params = urllib.parse.urlencode({'sn': self.device_id, 'key': self.device_key})
    try:
      f = urllib.request.urlopen("https://sensor.insgroup.fr/iot/devices/crc.json?%s" % token_params)
    except urllib.error.HTTPError as err:
      self.lastHTTPError = err.code
      return 0
    except:
      return 0
    # read and check token
    self.token = f.read()
    return 1

  def print_token(self):
    print("token (base64)  : %s" % self.token.decode('ascii'))
