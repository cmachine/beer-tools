import requests, json

url = 'http://api.brewerydb.com/v2'
key = '8598adbbb6bd20ddd9c453876b6385e9'
params = {'key':'8598adbbb6bd20ddd9c453876b6385e9'}

def getLocationByZip(zip):
  locatonUrl = '{0}/locations'.format(url)
  params['postalCode'] = zip
  response = requests.get(locatonUrl, params=params)
  return(json.loads(response.text))

concordZips = ['94521','94522','94518','94519','94520','94524','94527','94529']
concordBreweries = {}

for zip in concordZips:
  concordBreweries[zip] = getLocationByZip(zip)

print json.dumps(concordBreweries, indent=4, sort_keys=True)


