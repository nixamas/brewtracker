# -*- coding: utf-8 -*-
"""
    Brew Buddy.
"""
from __future__ import with_statement
from OpenBeerDataBaseAPI import Beer_Database_Api
from datacapture import get_temperature
from flask import Flask, request, session, redirect, url_for, render_template, flash, _app_ctx_stack
from jsonencoder import build_json
from sqlite3 import dbapi2 as sqlite3
import SystemSettings
import json

# configuration
DATABASE = 'brewtrackerdb.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
CONFIG_FILE = 'config'

BEER_DATABASE = {}

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect(app.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db

    return top.sqlite_db

@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()

@app.route('/')
@app.route('/index')
@app.route('/analysis', methods=['GET'])
def show_analysis():
    db = get_db()
    cur = db.execute('select id, reading_time, reading_brew_temp, reading_amb_temp from readings order by id asc')
    readings = cur.fetchall()
    readings_array_list = []
    for reading in readings:
        r = ( reading[0], str(reading[1]), str(reading[2]), str(reading[3]) )
        print(str(r))
        readings_array_list.append(r)
    return render_template('analysis.html', readings=json.loads(build_json()) )

@app.route('/beers', methods=['GET'])
def show_beers():
    beers = BEER_DATABASE.get_beers()
    beers_json = json.dumps(beers)
    return render_template('beerlist.html', beers=beers_json)    

@app.route('/brewery/<int:brewery_id>', methods=['GET'])
def show_brewery(brewery_id):
    brewery = BEER_DATABASE.get_brewery(brewery_id)
    brewery_beers = BEER_DATABASE.get_beers_from_brewery(brewery_id)
    brewery_beers_json = json.dumps(brewery_beers)
    return render_template('brewery.html', brewery_name=brewery['name'], brewery_url=brewery['url'], brewery_beers=brewery_beers_json)

@app.route('/debug', methods=['GET', 'POST'])
def show_debug():
    debug_data = '{"temp":"' + str(get_temperature()) +'"}'
    return json.dumps(debug_data)
    
@app.route('/admin', methods=['GET', 'POST'])
def show_admin():
    error = None
    if request.method == 'POST':
        print("post recieved for admin")    #Changing system settings
        print("desired_temp :: " + str(request.form['desired_temp']))
        SystemSettings.set_desired_temp( request.form['desired_temp'])
        print("range :: " + str(request.form['range']))
        SystemSettings.set_range( request.form['range'])
        print("reading :: " + str(request.form['reading_interval']))
        SystemSettings.set_reading_interval( request.form['reading_interval'] )
        print("admin_email :: " + str(request.form['admin_email']))
        SystemSettings.set_admin_email( request.form['admin_email'])
        flash('Admin Settings Changed')
        return redirect(url_for('show_admin'))
    return render_template('admin.html', 
                           error=error, 
                           desired_temp=SystemSettings.get_desired_temp(), 
                           range=SystemSettings.get_range(), 
                           reading_interval=SystemSettings.get_reading_interval(), 
                           admin_email=SystemSettings.get_admin_email())

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_admin'))
    return render_template('admin.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries')) 

if __name__ == '__main__':
    init_db()
    if BEER_DATABASE == {} :
        BEER_DATABASE = Beer_Database_Api()
        
    app.run()
    
    #enable server to listen on ip's
    #app.run(host='0.0.0.0')
    
    
    
    
    
    
