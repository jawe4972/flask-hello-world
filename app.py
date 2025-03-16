from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World! from Jason Terrance Wells, MD in 3308'
