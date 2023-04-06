from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                         # which is made by invoking the function Bcrypt with our app as an argument

@app.route('/') # default route loads index.html
def load_index():
    if 'user_id' in session:
        return redirect(f"/dashboard/{session['user_id']}")
    if 'in_progress' in session:
        in_progress = session['in_progress']
    else:
        in_progress = {}
    return render_template('index.html', in_progress = in_progress)
@app.route('/register/process', methods=['POST'])
def process_registration():
    if not User.validate_registration(request.form):
        session['in_progress'] = request.form # save progress so user doesn't have to re-enter everything
        return redirect('/')
    # if valid:
    if 'in_progress' in session:
        session.pop('in_progress') # delete form progress
    # hash password
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # probably best practice to make a db column for each strategy and store
    # a boolean for each one selected. Here, I just want to gather them.
    data = { # request.form is a tuple, and can't be edited, so create a dict to hold password hash and strategies string
        'fname': request.form['fname'],
        'lname': request.form['lname'],
        'email': request.form['email'],
        'password': pw_hash,
        'birthday': request.form['birthday'],
        'lang': request.form['lang'],
        'os': request.form['os'],
        'subscription': int(request.form['subscribe']) if 'subscribe' in request.form else 0
    }
    new_user_id = User.add_new_user(data)
    # set session with new ID
    session['user_id'] = new_user_id
    # redirect to dashboard
    return redirect(f"/dashboard/{new_user_id}")
@app.route('/login/process', methods=['POST'])
def process_login():
    # check if user is in the database
    user_in_db = User.get_user_by_email({'email': request.form['email']})
    if not user_in_db:
        flash('Invalid Email/Password.', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get false on password check:
        flash('Invalid Email/Password.', 'login')
        return redirect('/')
    # if they match, load the dashboard!
    session['user_id'] = user_in_db.id
    return redirect(f"/dashboard/{user_in_db.id}")
@app.route('/dashboard/<int:id>')
def load_user_dashboard(id):
    if 'user_id' not in session:
        return redirect('/')
    # get user data to personalize dashboard
    user_data = User.get_user_data({'id': session['user_id']})
    return render_template('dashboard.html', user = user_data)
@app.route('/update_subscription', methods=['POST'])
def update_subscription():
    toggle = 1 if 'subscribe' in request.form else 0
    User.update_subscription({'id': request.form['id'], 'subscribe': toggle})
    message = 'Subscribed' if 'subscribe' in request.form else 'You unsubscribed. Please come back.'
    flash(message, 'subscribe')
    return redirect(f"/dashboard/{request.form['id']}")
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')