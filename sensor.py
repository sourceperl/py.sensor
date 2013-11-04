#!/usr/bin/python

# 
# Python class for interface with Telecom Design Sensor platform
# Test with Python2.7 and Python3
#
# Think to add request to your Python install
# on debian like : 
# $ sudo apt-get install python-requests python3-requests
# you can also use pip :
# $ sudo pip install requests
# 
# code under GPLv2

# some libs
import requests

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
    headers = {'Authorization: Basic ': self.auth_token}
    r = requests.get("https://sensor.insgroup.fr/iot/developers/apps.json", 
                     headers=headers, )
    # check error status
    if(r.status_code != requests.codes.ok):
      return 0
    # return decode JSON string
    return r.json()
  
  def mod_register(self, mod_serial, mod_key):
    """
    Attach a single or multiple module(s) to the developer's account
      return an array of modules if success
      return 0 if fail
    """
    headers = {'Authorization: Basic ': self.auth_token,
               'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'serial': str(mod_serial), 'key': str(mode_key)}
#    params = "[{\"serial\": \"" + str(mod_serial) + 
#             "\", \"key\": \"" + str(mod_key) + "\"}]"
    r = requests.post("https://sensor.insgroup.fr/iot/developers/modules.json",
                      params=params, headers=headers)
    # check error status
    if(r.status_code != requests.codes.ok):
      return 0
    # return decode JSON string
    return r.json()

  def mod_list(self):
    """
    Get modules list for this developer account
      return an array of modules if success
      return 0 if fail
    """
    headers = {'Authorization: Basic ': self.auth_token}
    r = requests.get("https://sensor.insgroup.fr/iot/developers/modules.json",
                     headers=headers)
    # check error status
    if(r.status_code != requests.codes.ok):
      return 0
    # return decode JSON string
    return r.json()

  def print_token(self):
    """Display token on stdout"""
    print("token (base64)  : %s" % self.auth_token.decode('ascii'))
  
  def _auth(self):
    """
    Get the auth token for current developer account
      return 1 if success
      return 0 if fail
    """
    params = {'login': self.auth_login, 'pwd': self.auth_pwd}
    r = requests.get("https://sensor.insgroup.fr/security/authentication",
                     params=params)
    # check error status
    if(r.status_code != requests.codes.ok):
      return 0
    # read and check token
    self.auth_token = r.text
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
    # make request
    params = {'sn': self.device_id, 'amount': amount}
    if (until > 0):
      params['until'] = until
    headers = {'X-Snsr-Device-Key': self.token}
    r = requests.get("https://sensor.insgroup.fr/iot/devices/msgs/history.json", 
                     params=params, headers=headers)
    # check error status
    if(r.status_code != requests.codes.ok):
      return 0
    # return decode JSON string
    return r.json()

  def get_information(self):
    """
    Get device information
      return an array of message if success
      return 0 if fail
    """
    # make request
    params = {'sn': self.device_id}
    headers = {'X-Snsr-Device-Key': self.token}
    r = requests.get("https://sensor.insgroup.fr/iot/devices/children.json", 
                 params=params, headers=headers)
    # check error status
    if(r.status_code != requests.codes.ok):
      return 0
    # return decode JSON string
    return r.json()
  
  def print_token(self):
    """Display token on stdout"""
    print("token (base64)  : %s" % self.token.decode('ascii'))

  def _update_token(self):
    """
    Get the token for current device id/key
      return 1 if success
      return 0 if fail
    """
    # make request
    params = {'sn': self.device_id, 'key': self.device_key}
    r = requests.get("https://sensor.insgroup.fr/iot/devices/crc.json", 
                     params=params)
    # check error status
    if(r.status_code != requests.codes.ok):
      return 0
    # read and check token
    self.token = r.text
    return 1
