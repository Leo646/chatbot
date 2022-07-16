import os
from tokenize import String
from flask import Flask, jsonify, render_template
from flask import request
#from chat import get_response

import random

app = Flask(__name__ )
@app.get("/")
def index():
    return render_template("index3.html")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=port)
