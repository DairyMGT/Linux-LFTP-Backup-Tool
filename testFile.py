import json
import datetime
import os
from backupTracker import  backupTracker

with open('config.json') as json_data_file:
    data = json.load(json_data_file)

print(data['includeDir'])

for x in data['includeDir']:
    print(x)

print(data['ftp']['host'])

# dateFormat =  str(date.today().year) + str(date.today().month) + str(date.today().day)
# print(dateFormat)

print(len(data['includeDir']))



def f(first, second=None):
  print(first, second)
  if(second):
    print(second)


f("abc", "cbd")


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

print(BASE_DIR)

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
deploymentHistoryList = BASE_DIR + "/deploymentHistoryList.json"

if ((os.path.isdir(deploymentHistoryList)) != True):
    data={'head': "0",
          'tail': "0",
          'packages':{
              #0: ['', '', ''] # compressed and dummp file names, date
          },
          }

    with open('deploymentHistoryList.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)



bt = backupTracker(["abc", "cbd"])