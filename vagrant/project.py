from flask import(Flask, render_template, request, redirect, url_for,
flash, jsonify, abort, g, make_response)
from flask import session as login_session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Item, Category

from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2, requests
import json, random, string

engine = create_engine('postgresql+psycopg2:///catalog')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Interview Practice"

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
        for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE = state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token from google
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError: #If exchange fails
        response = make_response(json.dumps('Failed to upgrade the auth code.'),
            401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
        access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    #If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
            "Token's user ID doesn't match given user ID.", 401))
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if already signed
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected'),
            200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get User Info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # See if user exists in db, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output

# Google Disconnect
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if(login_session['provider'] == 'google'):
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out")
        return redirect(url_for('showAllCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showAllCategories'))

def createUser(login_session):
    newUser = User(name = login_session['username'],
        email = login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id = user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Home Page
@app.route('/')
@app.route('/catalog')
def showAllCategories():
    category = session.query(Category).all()
    return render_template('home.html', categories=category, login_session=login_session)

# Category CREATE
@app.route('/catalog/new', methods=['GET', 'POST'])
def createCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if not request.form['name'] and not request.form['description']:
            flash("Please fill out the form please!")
            return render_template("createCategory.html")
        category=Category(name=request.form['name'],
            description=request.form['description'], user_id=login_session['user_id'])
        session.add(category)
        session.commit()
        flash('Category Successfully Added')
        return redirect(url_for("showAllCategories"))
    else:
        return render_template('createCategory.html')

# Category READ
@app.route('/catalog/<category_name>/items')
def showCategoryItems(category_name):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name = category_name).one()
    items = session.query(Item).filter_by(category_id = category.id).all()
    return render_template(
            'showItems.html',
            items = items,
            category = category,
            categories=categories,
            login_session=login_session
            )

# Category UPDATE
@app.route('/catalog/<category_name>/edit', methods=['GET', 'POST'])
def editCategory(category_name):
    if 'username' not in login_session:
        return redirect('/login')
    editedCategory = session.query(Category).filter_by(name = category_name).one()
    if login_session['user_id'] != editedCategory.user_id:
        return "<script>function myFunction(){alert('You are not authorized to edit this category.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
        if request.form['description']:
            editedCategory.description = request.form['description']
        session.add(editedCategory)
        session.commit()
        flash("Category Successfully Edited")
        return redirect(url_for('showAllCategories'))
    else:
        return render_template('editCategory.html', category=editedCategory)

# Category DELETE
@app.route('/catalog/<category_name>/delete', methods=['GET', 'POST'])
def deleteCategory(category_name):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(name=category_name).one()
    if login_session['user_id'] != category.user_id:
        return "<script>function myFunction(){alert('You are not authorized to edit this category.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(category)
        session.commit()
        flash('%s Successfully Deleted' % category.name)
        return redirect(url_for('showAllCategories'))
    else:
        return render_template('deleteCategory.html', category=category)

# ITEM CREATE
@app.route('/catalog/<category_name>/items/new', methods=['GET', 'POST'])
def createItem(category_name):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == "POST":
        category = session.query(Category).filter_by(name=category_name).one()
        if not request.form['name'] and not request.form['description']:
            flash("Please fill out the form please!")
            return render_template("createItem.html", category_name=category_name)
        newItem = Item(
            name=request.form['name'],
            description=request.form['description'],
            user_id=login_session['user_id'],
            category_id=category.id
            )
        session.add(newItem)
        session.commit()
        flash('New Item %s Successfully Created' % newItem.name)
        return redirect(url_for('showCategoryItems', category_name=category_name))
    else:
        return render_template('createItem.html', category_name=category_name)

# Item READ
@app.route('/catalog/<category_name>/<item_name>')
def showItem(category_name, item_name):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name = category_name).one()
    item = session.query(Item).filter_by(name=item_name, category_id=category.id).one()
    return render_template(
            'item_page.html',
            category=category,
            item=item,
            categories=categories,
            login_session=login_session
            )

# ITEM UPDATE
@app.route('/catalog/<category_name>/<item_name>/edit/', methods=['GET', 'POST'])
def editItem(category_name, item_name):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(name=category_name).one()
    editedItem = session.query(Item).filter_by(name=item_name, category_id=category.id).one()
    if login_session['user_id'] != editedItem.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit menu items to this restaurant. Please create your own restaurant in order to edit items.');}</script><body onload='myFunction()'>"
    if request.method == "POST":
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash('Item Successfully Edited')
        return redirect(url_for('showCategoryItems', category_name=category.name))
    else:
        return render_template('editItem.html', category=category, item=editedItem)

# ITEM DELETE
@app.route('/catalog/<category_name>/<item_name>/delete/', methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(name=category_name).one()
    deleteItem = session.query(Item).filter_by(name=item_name, category_id=category.id).one()
    if login_session['user_id'] != deleteItem.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit menu items to this restaurant. Please create your own restaurant in order to edit items.');}</script><body onload='myFunction()'>"
    if request.method == "POST":
        session.delete(deleteItem)
        session.commit()
        flash("Item Successfully Deleted")
        return redirect(url_for('showCategoryItems', category_name=category.name))
    else:
        return render_template('deleteItem.html', category=category, item=deleteItem)

# API ENDPOINTS

# Endpoint for info all interview topics
@app.route('/catalog/JSON')
def allCategoryJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])

# Endpoint for info of one category
@app.route('/catalog/<category_name>/JSON')
def categoryJSON(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    return jsonify(category=category.serialize)

# Endpoint for info of all problems from a category
@app.route('/catalog/<category_name>/items/JSON')
def categoryItemsJSON(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id = category.id).all()
    return jsonify(items=[i.serialize for i in items])

# Endpoint for info of one problem from a category
@app.route('/catalog/<category_name>/<item_name>/JSON')
def itemJSON(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(name=item_name,
        category_id=category.id).one()
    return jsonify(item=item.serialize)




if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
