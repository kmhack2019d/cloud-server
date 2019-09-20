from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"hello": "world"})

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
