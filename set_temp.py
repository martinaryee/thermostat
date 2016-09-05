import nest
import json
import glob
import urllib2
from time import gmtime, strftime
from nest import utils as nest_utils
import argparse

parser = argparse.ArgumentParser(description='Set temp')
parser.add_argument('device_room_target_temp', type=float)
args = parser.parse_args()
device_room_target_temp = nest_utils.f_to_c(args.device_room_target_temp)

#device_room_target_temp = 73
#device_room_target_temp = nest_utils.f_to_c(device_room_target_temp)

min_diff_to_alter_temp = 1 / 1.8

# Read Nest sensors
print 'Reading Nest sensors'
username = 'martin.aryee@gmail.com'
password = 'Ma770522'
napi = nest.Nest(username, password)
structure = napi.structures[0]
nest = structure.devices[0]

# Read device room temp
print 'Reading PEP sensors'
str_data=urllib2.urlopen("http://10.0.1.11/temp").read()
device_temp = float(str_data.split(",")[0])

temp_diff = device_temp - nest.temperature
new_nest_target = device_room_target_temp - temp_diff
target_diff = new_nest_target - nest.target

print 'Current device room temperature : %0.1f' % nest_utils.c_to_f(device_temp)
print 'Current Nest temperature: %0.1f' % nest_utils.c_to_f(nest.temperature)
print 'Temperature diff: %0.1f' % (temp_diff * 1.8)

print 'Current Nest target: %0.1f' % nest_utils.c_to_f(nest.target)
print 'Current device room target : %0.1f' % nest_utils.c_to_f(device_room_target_temp)
print 'New Nest target: %0.1f' % nest_utils.c_to_f(new_nest_target)
print 'Target difference: %0.1f' % (target_diff * 1.8)


if abs(target_diff) > min_diff_to_alter_temp:
    print 'Setting Nest temp to  %0.1f in order to achieve %0.1f in device room' % (nest_utils.c_to_f(new_nest_target), nest_utils.c_to_f(device_room_target_temp))
    #nest.target = new_nest_target
else:
    print 'Leaving temp unchanged'


