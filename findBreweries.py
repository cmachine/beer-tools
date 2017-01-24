import requests, json, flask, uuid, pprint
from flask import Flask, session
app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

url = 'http://api.brewerydb.com/v2'
key = '8598adbbb6bd20ddd9c453876b6385e9'

@app.route("/")
def home():
  return flask.render_template('index.html')

@app.route('/info')
def info():
  info = {}
  name = flask.request.args.get('name')
  for brewery in session['breweries']:
    print brewery['brewery']['name']
    if brewery['brewery']['name'] == name:
      info['name'] = brewery['brewery']['name']
      info['website'] = brewery['brewery']['website']
      info['streetAddress'] = brewery['streetAddress']
      info['description'] = brewery['brewery']['description']
  return flask.render_template('info.html', info=info, name=name)


@app.route('/find', methods = ['POST'])
def find():
  location = {
    'state':flask.request.form['state'],
    'city': flask.request.form['city'],
    'zip':flask.request.form['zip']
  }
  breweries=getDataForLocation(location)
  session.clear()
  session['breweries'] = breweries
  names = getBreweryNames(breweries)
  return flask.render_template('index.html', names=names)

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
    if 'brewery' in brewery:
      names.append((brewery['brewery']['name']))
  return names

def getBreweryFromData(breweryData, name):
  for brewery in breweryData:
    if brewery['name'] == name:
      return brewery


if __name__ == "__main__":
  app.debug = True
  app.run(host='0.0.0.0', port=80)

