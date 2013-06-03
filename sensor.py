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

class Developer:
  """
  Python module for interface with Telecom Design Sensor Web services
  Developer class

  usage sample:
    devel = Developer()
    devel.login(login, password)
  """

  def __init__(self):
    """Class builder"""
    self.auth_token    = ''
    self.auth_login    = ''
    self.auth_pwd      = ''
    self.lastHTTPError = 0
  
  def login(self, dev_login, dev_password):
    """
    Login to developer account
      return 1 if success
      return 0 if fail
    """
    self.auth_login = dev_login
    self.auth_pwd   = dev_password
    return self._auth()

  def app_list(self):
    """
    Get app list for this developer account
      return an array of app if success
      return 0 if fail
    """
    try:
      req = urllib.request.Request("https://sensor.insgroup.fr/iot/developers/apps.json")
      # don't work if white space after 'Basic' is remove
      req.add_header('Authorization: Basic ', self.auth_token)
      f = urllib.request.urlopen(req)
    except urllib.error.HTTPError as err:
      self.lastHTTPError = err.code
      return 0
    except:
      return 0
    app_json = f.read()
    apps = json.loads(app_json.decode('ascii'))
    return apps
  
  def mod_list(self):
    """
    Get modules list for this developer account
      return an array of modules if success
      return 0 if fail
    """
    try:
      req = urllib.request.Request("https://sensor.insgroup.fr/iot/developers/modules.json")
      # don't work if white space after 'Basic' is remove
      req.add_header('Authorization: Basic ', self.auth_token)
      f = urllib.request.urlopen(req)
    except urllib.error.HTTPError as err:
      self.lastHTTPError = err.code
      return 0
    except:
      return 0
    mod_json = f.read()
    mods = json.loads(mod_json.decode('ascii'))
    return mods

  def print_token(self):
    """Display token on stdout"""
    print("token (base64)  : %s" % self.auth_token.decode('ascii'))
  
  def _auth(self):
    """
    Get the auth token for current developer account
      return 1 if success
      return 0 if fail
    """
    auth_params = urllib.parse.urlencode({'login': self.auth_login, 'pwd': self.auth_pwd})
    try:
      f = urllib.request.urlopen("https://sensor.insgroup.fr/security/authentication?%s" % auth_params)
    except urllib.error.HTTPError as err:
      self.lastHTTPError = err.code
      return 0
    except:
      return 0
    # read and check token
    self.auth_token = f.read()
    return 1

class Device:
  """
  Python module for interface with Telecom Design Sensor Web services
  Device class

  usage sample:
    device = Device()
    device.set_device(your_id, your_key)
    msgs = device.get_last_msgs(30)
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
    Get messages history
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

  def get_information(self):
    """
    Get device information
      return an array of message if success
      return 0 if fail
    """
    params = {'sn': self.device_id}
    msg_params = urllib.parse.urlencode(params)
    try:
      req = urllib.request.Request("https://sensor.insgroup.fr/iot/devices/children.json?%s" % msg_params)
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
  
  def print_token(self):
    """Display token on stdout"""
    print("token (base64)  : %s" % self.token.decode('ascii'))

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
