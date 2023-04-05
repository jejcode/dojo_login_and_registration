from flask import Flask # import Flask to create an instance app
app = Flask(__name__) # create instance of Flask
app.secret_key="My keys are so insecure right now." # session and flash need secret_key to work