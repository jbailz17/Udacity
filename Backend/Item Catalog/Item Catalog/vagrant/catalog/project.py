#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, jsonify, url_for,\
        flash

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Connect database and create database session
engine = create_engine('sqlite:///project.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Login page (login with FB or Google)
@app.route('/login')
def showLogin():
    # create a session state
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for
                    x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Login for google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Check the login state matches the state sent through request
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data
    try:
        # Upgrade the authorization code into a credentials object.
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps
                                 ('Failed to upgrade the authorization code.'))
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = 'https://www.googleapis.com/oauth2/v1/'
    url += 'tokeninfo?access_token=%s' % access_token
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))

    # Check for error in access_token
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    # Check to see if user is already connected.
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['provider'] = "google"
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if user_id is None:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    print(user_id)

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;border-radius:
              150px;-webkit-border-radius: 150px;-moz-border-radius:
              150px;"> '''

    flash("You are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


# Disconnect from google
@app.route("/gdisconnect")
def gdisconnect():
    access_token = ""
    access_token = login_session['credentials']
    # Check to see if user is connected.
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Revoke access token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(
            json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# Connect to Facebook
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application.json'
        return response

    # Obtain short term token
    access_token = request.data.decode("utf-8")

    app_id = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_'
    url += 'exchange_token&client_id={}&client_secret={}&fb_exchange_token={}'\
           .format(app_id, app_secret, access_token)

    # Obtain long term token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result.decode('utf-8'))
    userinfo_url = "https://graph.facebook.com/v2.10/me"
    token = 'access_token=' + data['access_token']

    # Obtain user info
    url = 'https://graph.facebook.com/v2.10/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))

    login_session['provider'] = "facebook"
    login_session['username'] = result['name']
    login_session['facebook_id'] = result['id']
    login_session['email'] = result['email']
    login_session['credentials'] = access_token

    # Obtain profile picture
    url = 'https://graph.facebook.com/v2.10/me/picture?%s&' % token
    url += 'redirect=0&height=200&width=200'
    print(url)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))

    login_session['picture'] = result['data']['url']

    user_id = getUserID(login_session['email'])
    if user_id is None:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    print(login_session['user_id'])

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;border-radius:
              150px;-webkit-border-radius: 150px;-moz-border-radius:
              150px;"> '''

    flash("You are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


# Disconnect from Facebook
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    url = 'https://graph.facebook.com/%s/permissions' % facebook_id
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['facebook_id']
    return "you have been logged out"


# Handle disconnect for both FB and google.
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == "google":
            gdisconnect()

        elif login_session['provider'] == "facebook":
            fbdisconnect()

        del login_session['provider']
        flash("Successfully Disconnected")
        return redirect('/')
    else:
        return redirect('/')


# Return catalog info in JSON
@app.route('/catalog/JSON')
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[i.serialize for i in categories])


# Return Item information in JSON
@app.route('/catalog/<int:category_id>/items/JSON')
def categoryItemsJSON(category_id):
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


# Show home catalog home page and latest items.
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Category).order_by(asc(Category.id))
    items = session.query(Item).order_by(desc(Item.id))
    if 'username' not in login_session:
        return render_template(
            'public_catalog.html', categories=categories, items=items)
    else:
        return render_template(
            'catalog.html', categories=categories, items=items)


# Show specific category with items.
@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/items/')
def showItems(category_id):
    categories = session.query(Category).order_by(asc(Category.id))
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    if 'username' not in login_session:
        return render_template(
            'public_items.html', category=category,
            categories=categories, items=items)
    else:
        current = getUserInfo(login_session['user_id'])
        creator = getUserInfo(category.user_id)
        return render_template(
            'items.html', category=category, categories=categories,
            items=items, current=current, creator=creator)


# Show specific item and description
@app.route('/catalog/<int:category_id>/<int:item_id>/')
def showItem(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return render_template('public_showItem.html', item=item)
    else:
        current = getUserInfo(login_session['user_id'])
        creator = getUserInfo(item.user_id)
        return render_template(
            'showItem.html', item=item, current=current, creator=creator)


# Create a new category
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    else:
        if request.method == 'POST':
            newCategory = Category(name=request.form['name'],
                                   user_id=login_session['user_id'])
            session.add(newCategory)
            session.commit()
            flash('New Category Successfully Created')
            return redirect(url_for('showCatalog'))
        else:
            return render_template('addCategory.html')


# Edit category details
@app.route('/catalog/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    elif category.user_id != login_session['user_id']:
        return """<script>
            function myFunction() {
                alert ('You are not authorized to edit this category');
            } </script><body onload='myFunction()'>"""
    else:
        if request.method == 'POST':
            if request.form['name']:
                category.name = request.form['name']
            session.add(category)
            session.commit()
            flash('%s Successfully Updated' % category.name)
            return redirect(url_for('showItems', category_id=category_id))
        else:
            return render_template('editCatalog.html', category=category)


# Delete category
@app.route('/catalog/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    elif category.user_id != login_session['user_id']:
        return """<script>
            function myFunction() {
                alert ('You are not authorized to delete this category');
            } </script><body onload='myFunction()'>"""
    else:
        if request.method == 'POST':
            session.delete(category)
            flash('%s Successfully Deleted' % category.name)
            session.commit()
            return redirect(url_for('showCatalog'))
        else:
            return render_template('deleteCatalog.html', category=category)


# Add a new item
@app.route('/catalog/<int:category_id>/items/new/', methods=['GET', 'POST'])
def newItem(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    else:
        if request.method == 'POST':
            newItem = Item(name=request.form['name'],
                           description=request.form['description'],
                           category_id=category_id,
                           user_id=login_session['user_id'])
            session.add(newItem)
            session.commit()
            flash('New Item Successfully Created')
            return redirect(url_for('showItems', category_id=category_id))
        else:
            return render_template('addItem.html', category_id=category_id)


# Edit item details
@app.route('/catalog/<int:category_id>/<int:item_id>/edit/',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    elif item.user_id != login_session['user_id']:
        return """<script>
            function myFunction() {
                alert ('You are not authorized to edit this item');
            } </script><body onload='myFunction()'>"""
    else:
        if request.method == 'POST':
            if request.form['name']:
                item.name = request.form['name']
            if request.form['description']:
                item.description = request.form['description']
            session.add(item)
            session.commit()
            flash('%s Successfully Updated' % item.name)
            return redirect(
                url_for('showItem', category_id=category_id, item_id=item_id))
        else:
            return render_template('editItem.html', item=item)


# Delete an item
@app.route('/catalog/<int:category_id>/<int:item_id>/delete/',
           methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    elif item.user_id != login_session['user_id']:
        return """<script>
            function myFunction() {
                alert ('You are not authorized to delete this item');
            } </script><body onload='myFunction()'>"""
    else:
        if request.method == 'POST':
            session.delete(item)
            flash('%s Succesfully Deleted' % item.name)
            session.commit()
            return redirect(url_for('showItems', category_id=category_id))
        else:
            return render_template(
                'deleteItem.html', item=item, category=category)


# Adding new user to the database.
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# Obtaining user info
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# Obtaining user ID
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
