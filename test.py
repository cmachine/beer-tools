import requests, json

url = 'http://api.brewerydb.com/v2'
key = '8598adbbb6bd20ddd9c453876b6385e9'
params = {'key':'8598adbbb6bd20ddd9c453876b6385e9'}

def getLocationByZip(zip):
  locatonUrl = '{0}/locations'.format(url)
  params['postalCode'] = zip
  response = requests.get(locatonUrl, params=params)
  parsed = json.loads(response.text)
  #todo handle multiple pages
  return(parsed['data'])

def getLocationByCityState(city, state):
  locatonUrl = '{0}/locations'.format(url)
  params['locality'] = city
  params['region'] = state
  response = requests.get(locatonUrl, params=params)
  parsed = json.loads(response.text)
  #todo handle multiple pages
  return(parsed['data'])

#concordZips = ['94521','94522','94518','94519','94520','94524','94527','94529']
concordLocations = getLocationByCityState('Concord','California')
for loc in concordLocations:
 if 'brewery' in loc:
   print  loc['brewery']['name']

#print json.dumps(concordLocations, indent=4, sort_keys=True)


