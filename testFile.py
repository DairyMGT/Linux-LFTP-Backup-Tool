import json
from datetime import date

with open('config.json') as json_data_file:
    data = json.load(json_data_file)

print(data['includeDir'])

for x in data['includeDir']:
    print(x)

print(data['ftp']['host'])

dateFormat =  str(date.today().year) + str(date.today().month) + str(date.today().day)
print(dateFormat)

print(len(data['includeDir']))



def f(first, second=None):
  print(first, second)
  if(second):
    print(second)


f("abc", "cbd")


f("abc Test")