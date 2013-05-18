# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import with_statement
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, _app_ctx_stack
from sqlite3 import dbapi2 as sqlite3
from beerdatabaseapiparser import Beer_Database_Api
from jsonencoder import build_json
import json 

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

BEER_DATABASE = {}

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


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
def show_entries():
    db = get_db()
    cur = db.execute('select reading_time, reading_brew_temp, reading_amb_temp from readings order by id desc')
    readings = cur.fetchall()
    return render_template('show_entries.html', readings=readings)

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
    bb = json.dumps(beers)
    return render_template('beerlist.html', beers=bb)    
    
@app.route('/admin', methods=['GET', 'POST'])
def show_admin():
    error = None
    if request.method == 'POST':
        print("post recieved for admin")
        print("interval :: " + str(request.form['interval']))
        print("adminemail :: " + str(request.form['adminemail']))
        flash('Admin Settings Changed')
        return redirect(url_for('show_analysis'))
    return render_template('admin.html', error=error)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into readings (reading_time, reading_brew_temp, reading_amb_temp) values (?, ?, ?)',
                 [request.form['reading_time'], request.form['reading_brew_temp'], request.form['reading_amb_temp']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


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
