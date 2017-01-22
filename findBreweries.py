import requests, json, flask
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
  return flask.render_template('index.html')

@app.route('/find', methods = ['POST'])
def find():
  state = flask.request.form['state']
  city = flask.request.form['city']
  loc = getLocationByCityState(city, state)
  names = getBreweryNames(loc)
  return flask.render_template('results.html', names=names)



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
  print city
  print state
  locatonUrl = '{0}/locations'.format(url)
  params['locality'] = city
  params['region'] = state
  response = requests.get(locatonUrl, params=params)
  parsed = json.loads(response.text)
  #todo handle multiple pages
  return(parsed['data'])

def getBreweryNames(location):
  names = []
  for loc in location:
    if 'brewery' in loc:
      names.append(loc['brewery']['name'])
  return names


if __name__ == "__main__":
  app.debug = True
  app.run(host='0.0.0.0', port=80)

