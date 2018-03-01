from flask import Flask
app = Flask(__name__)
import os

@app.route('/')
def index():
    return 'Yo, its working!'

@app.route('/yo')
def yo():
    return '<h1>ёпта, чезах</h1>'

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)