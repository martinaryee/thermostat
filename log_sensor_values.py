import nest
import json
import glob
import urllib2
from time import gmtime, strftime


def log(publicKey, privateKey, field, value):
    url = "https://data.sparkfun.com/input/%s?private_key=%s&%s=%s" % (publicKey, privateKey, field, value)
    return_code = urllib2.urlopen(url).read()
    return return_code


print '------------------------------------------------------------'
print strftime("%Y-%m-%d %H:%M:%S", gmtime())

# Read Nest sensors
print 'Reading Nest sensors'
username = 'martin.aryee@gmail.com'
password = 'Ma770522'
napi = nest.Nest(username, password)
structure = napi.structures[0]
device = structure.devices[0]

# Read other sensors
print 'Reading PEP sensors'
str_data=urllib2.urlopen("http://10.0.1.11/temp").read()
pep0_temp = str_data.split(",")[0]

sensors = [
        {'name': '02138 temperature', 
            'conf':  'sparkfun/keys_AJ57EDv0W8t1lMjKLJE5.json',
            'key': 'temp',
            'value': str(structure.weather.current.temperature)
        },
        {'name': '02138 humidity',
            'conf':  'sparkfun/keys_jqyJ09QJvYtvVgKGWMW9.json',
            'key': 'humidity',
            'value': str(structure.weather.current.humidity)
        },    
        {'name': 'Nest mode',
            'conf':  'sparkfun/keys_q5wNxKdgvbuxrXlo4pAd.json',
            'key': 'mode',
            'value': device.mode
        },    
        {'name': 'Dining room temperature (Nest)',
            'conf':  'sparkfun/keys_0lg42LbMzwCy953NOxJn.json',
            'key': 'temp',
            'value': str(device.temperature)
        },    
        {'name': 'Dining room humidity (Nest)',
            'conf':  'sparkfun/keys_AJ5KnxyZJ1InXpdJdjV3.json',
            'key': 'humidity',
            'value': str(device.humidity)
        },    
        {'name': 'Target temperature (Nest)',
            'conf':  'sparkfun/keys_v0b32LwOJ3fEZKOQ25pw.json',
            'key': 'temp',
            'value': str(device.target)
        },
        #{'name': 'Dining room temperature (pep)',
        #    'conf': 'sparkfun/keys_aGrQExlQKEI3xRM5z363.json',
        #    'key': 'temp',
        #    'value': pep0_temp
        #},    
        {'name': 'Small bedroom temperature (pep)',
            'conf': 'sparkfun/keys_8djvJjbo2ESL5wm2p6yY.json',
            'key': 'temp',
            'value': pep0_temp
        }

]



for sensor in sensors:
    conf = json.load(open(sensor['conf']))
    print "%s: %s" % (sensor['name'], sensor['value']),
    try:
        msg = log(conf['publicKey'], conf['privateKey'], sensor['key'], sensor['value'])
        print ' - Logging status: %s' % msg,
    except:
        print 'FAILED'


#print 'Outside temp: %s' % structure.weather.current.temperature
#print 'Outside humidity: %s' % structure.weather.current.humidity
#print 'Nest mode: %s' % device.mode
#print 'Dining room temperature (Nest): %0.1f' % device.temperature
#print 'Dining room humidity (Nest): %0.1f' % device.humidity
#print 'Target temperature (Nest): %0.1f' % device.target

