import requests, json, flask
from flask import Flask
app = Flask(__name__)

url = 'http://api.brewerydb.com/v2'
key = '8598adbbb6bd20ddd9c453876b6385e9'

@app.route("/")
def home():
  return flask.render_template('index.html')

@app.route('/find', methods = ['POST'])
def find():
  location = {
    'state':flask.request.form['state'],
    'city': flask.request.form['city'],
    'zip':flask.request.form['zip']
  }
  print 'at find location={0}'.format(location)
  breweries=getBreweryNamesForLocation(location)
  return flask.render_template('index.html', names=breweries)

# Make a GET but catch errors
def safeGet(url, headers=None, params=None):
  try:
    response = requests.get(url,headers=headers, params=params, timeout=8)
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

def getDataForLocation(location):
  print 'at getDataForLocation location={0}'.format(location)
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
  print params
  data = getAllPages(locatonUrl, params)
  return data

def getBreweryNamesForLocation(location):
  print 'at getBreweryNamesForLocation location={0}'.format(location)

  data = getDataForLocation(location)
  if not data:
    return None
  return  getBreweryNames(data)

def getBreweryNames(breweries):
  names = []
  for brewery in breweries:
    if 'brewery' in brewery:
      names.append(brewery['brewery']['name'])
  return names


if __name__ == "__main__":
  app.debug = True
  app.run(host='0.0.0.0', port=80)

