from flask_app import app # import app so controllers can use it

# import controllers
from flask_app.controllers import users # routes for users table

if __name__ == '__main__': # make sure a module isn't running the app
    app.run(debug = True, port = 5001) # run in debug mode on port 5001 because 5000 is taken