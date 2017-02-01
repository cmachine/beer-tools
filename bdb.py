import requests, json

# Make a GET but catch errors
def safeGet(url, headers=None, params=None):
  try:
    response = requests.get(url,headers=headers, params=params, timeout=10)
    if response.status_code != 200:
      print "get returned {0}\nURL: {1}\nparams: {2}\ntext: {3}".format(response.status_code, url, params, response.text)
      return None
    return response
  except requests.exceptions.RequestException as e:
    print e
    return None

def getAllPages(url, params):
  page = 1
  total = 1
  data = []
  while page <= total:
    params['p'] = page
    response = safeGet(url, params=params)
    try:
      responseDict = json.loads(response.text)
      data = data + responseDict['data']
      page = responseDict['currentPage']
      total = responseDict['numberOfPages']
    except:
      return None
    page = page + 1
  return data

def getDataForSearch(query, type):
  searchUrl = '{0}/search'.format(url)
  params = {'q': query, 'type': type}
  params['key'] = key
  data = getAllPages(searchUrl, params)
  return data

def getDataForLocation(location):
  locatonUrl = '{0}/locations'.format(url)
  params = {}
  if location['zip']:
    params['postalCode'] = location['zip']
  if location['city']:
    params['locality'] = location['city']
  if location['state']:
    params['region'] =  location['state']
  params['isClosed'] = 'N'
  params['key'] = key
  data = getAllPages(locatonUrl, params)
  return data

def getBreweryNames(breweryData):
  names = []
  for brewery in breweryData:
    if 'name' in brewery:
      names.append(brewery['name'])
  return names

def getBeerNames(beerData):
  names = []
  for beer in beerData:
    if 'name' in beer:
      names.append(beer['name'])
  return names

def getBreweryFromData(breweryData, name):
  for brewery in breweryData:
    if brewery['name'] == name:
      return brewery