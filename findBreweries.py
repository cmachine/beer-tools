import flask, uuid, bdb
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
    if brewery['name'] == name:
      info['name'] = brewery['name']
      info['website'] = brewery['website']
      info['description'] = brewery['description']
      # loation data
      #info['streetAddress'] = brewery['streetAddress']
  return flask.render_template('info.html', info=info, name=name)

@app.route('/search', methods=['POST'])
def search():
  query = flask.request.form['query']
  type = flask.request.form['type']
  searchData = bdb.getDataForSearch(query, type)
  session.clear()
  if type == 'Beer':
    session['beers'] = searchData
    names = bdb.getBeerNames(searchData)
  else:
    session['breweries'] = searchData
    names = bdb.getBreweryNames(searchData)
  return flask.render_template('index.html', names=names)

@app.route('/find', methods = ['POST'])
def find():
  location = {
    'state':flask.request.form['state'],
    'city': flask.request.form['city'],
    'zip':flask.request.form['zip']
  }
  locationData = bdb.getDataForLocation(location)
  breweries = bdb.getBreweriesFromLocations(locationData)
  session.clear()
  session['breweries'] = breweries
  names = bdb.getBreweryNames(breweries)
  return flask.render_template('index.html', names=names)

def getBreweriesFromLocations(locations):
  breweries = []
  for location in locations:
    if 'brewery' in location:
      breweries.append(location['brewery'])
  return breweries





if __name__ == "__main__":
  app.debug = True
  app.run(host='0.0.0.0', port=80)

