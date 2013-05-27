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
from BrewTrackerDataBaseHandler import HomeBrewTrackerDataBase
from werkzeug.datastructures import ImmutableMultiDict
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
    #db = get_db()
    #cur = db.execute('select id, reading_time, reading_brew_temp, reading_amb_temp from readings order by id asc')
    #readings = cur.fetchall()
    #readings_array_list = []
    #for reading in readings:
    #    r = ( reading[0], str(reading[1]), str(reading[2]), str(reading[3]) )
    #    print(str(r))
    #    readings_array_list.append(r)
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

@app.route('/mybrews', methods=['GET'])
def show_my_brews():
    handler = HomeBrewTrackerDataBase()
    my_brews = handler.get_all_my_brews()
    
    return render_template( 'mybrews.html', my_brews=json.dumps(my_brews))

@app.route('/mybrew/<my_brew_id>', methods=['GET', 'POST'])
def show_my_brew(my_brew_id=None):
    handler = HomeBrewTrackerDataBase()
    print("******************")
    print(str(request))
    print("******************")
    if request.method == 'GET':
        if my_brew_id:
            my_brew = handler.get_beer_by_id(my_brew_id)
            return render_template( 'mybrew.html', brew_id=str(my_brew[0]), name=str(my_brew[1]), ingredients=str(my_brew[2]), brew_date=str(my_brew[3]), second_stage_date=str(my_brew[4]), bottle_date=str(my_brew[5]), abv=str(my_brew[6]), volume_brewed=str(my_brew[7]), notes=str(my_brew[8]) )#
        else:
            return render_template( 'mybrew.html', brew_id=str("-1"), name=str(""), ingredients=str(""), brew_date=str(""), second_stage_date=str(""), bottle_date=str(""), abv=str(""), volume_brewed=str(""), notes=str("") )
    elif request.method == 'POST':
        flash('Data updated...')
        handler.update_my_beer(my_brew_id, request.form['name'], request.form['ingredients'], request.form['brew_date'], request.form['second_stage_date'], request.form['bottle_date'], request.form['abv'], request.form['volume_brewed'], request.form['notes'])
        return render_template( 'mybrew.html', brew_id=str(my_brew_id), name=str(request.form['name']), ingredients=str(request.form['ingredients']), 
                                brew_date=str(request.form['brew_date']), second_stage_date=str(request.form['second_stage_date']), bottle_date=str(request.form['bottle_date']), 
                                abv=str(request.form['abv']), volume_brewed=str(request.form['volume_brewed']), notes=str(request.form['notes']) )

@app.route('/addbrew', methods=['GET','POST'])
def add_brew():
    print("adding brew")
    handler = HomeBrewTrackerDataBase()
    if request.method == 'POST':
        flash('New Brew was created')
        new_brew_id = handler.create_new_beer(request.form['name'], request.form['ingredients'], request.form['brew_date'], request.form['second_stage_date'], request.form['bottle_date'], request.form['abv'], request.form['volume_brewed'], request.form['notes'])
        return redirect(url_for('show_my_brew', my_brew_id=new_brew_id))
        #return render_template( 'mybrew.html', brew_id=str(request.form['name']), name=str(request.form['name']), ingredients=str(request.form['ingredients']), 
        #                        brew_date=str(request.form['brew_date']), second_stage_date=str(request.form['second_stage_date']), bottle_date=str(request.form['bottle_date']), 
        #                        abv=str(request.form['abv']), volume_brewed=str(request.form['volume_brewed']), notes=str(request.form['notes']) )
    else:   #Show an empty template page, allowing user to create a new brew
        return render_template( 'addbrew.html', brew_id=str("-1"), name=str(""), ingredients=str(""), brew_date=str(""), second_stage_date=str(""), bottle_date=str(""), abv=str(""), volume_brewed=str(""), notes=str("") )

@app.route('/deletebrew/<my_brew_id>', methods=['GET'])
def delete_brew(my_brew_id):
    print("deleting brew ::: " + str(my_brew_id))
    handler = HomeBrewTrackerDataBase()
    handler.delete_brew(my_brew_id)
    return redirect(url_for('show_my_brews'))

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
#    if BEER_DATABASE == {} :
#        BEER_DATABASE = Beer_Database_Api()
        
    app.run()
    
    #enable server to listen on ip's
    #app.run(host='0.0.0.0')
    
    
    
    
    
    
