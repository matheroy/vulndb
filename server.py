import requests
from flask import Flask, request, jsonify
import test_utils


app = Flask(__name__)

@app.route('/')
def hello():
    return "hello world"

@app.route('/test')
def test():
    return jsonify(test_utils.run())

if __name__ == '__main__':
    app.run(port='9000')
    
