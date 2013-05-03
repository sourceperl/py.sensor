#!/usr/bin/python3

#
# test script for sensor module : Developer class
#
# code under GPLv2

# some libs
import sensor
import time

# some private const (no push to public repo)
import private
DEVEL_LOGIN    = private.DEVEL_LOGIN
DEVEL_PASSWORD = private.DEVEL_PASSWORD

# use sensor object
devel = sensor.Developer()
# get token
if (not devel.login(DEVEL_LOGIN, DEVEL_PASSWORD)):
  print('login ko !')
  exit(1)

# get message history
apps = devel.app_list()
# skip if error
if apps == 0:
  print('retrieve apps ko !')
  exit(2)

print(apps)
exit(0)
