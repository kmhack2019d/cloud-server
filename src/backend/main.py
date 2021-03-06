from flask import Flask, jsonify, render_template
import get_data
import overlay
import json

app = Flask(__name__, static_folder='static', static_url_path='/', template_folder="static")

@app.route('/api/v1/get_data')
def getData():
    raspi = 0
    json_data = 0
    with open("./temp/data"+str(raspi)+".json", 'r') as fp:
        json_data = json.load(fp)
    return jsonify(json_data)

@app.route('/api/v1/get_image')
def getImage():
    raspi = 0
    json_data = 0
    with open("./temp/data"+str(raspi)+".json", 'r') as fp:
        json_data = json.load(fp)

    max_value = -1
    for d in json_data[0]["data"][0:5]:
        if max_value < d["value"]:
            max_value = d["value"]

    if (raspi == 0):
        overlay.overlay(0, "maps/0.jpg", [
            {
                "top": 370,
                "left": 810,
                "radiusH": 50,
                "radiusV": 50,
                "level": max_value / 100
            }
        ])

    return app.send_static_file('tempfiles/output_'+str(raspi)+'.jpg')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/<id>')
def detail(id):
    return render_template("index.html")

if __name__ == '__main__':
    print (app.url_map)
    app.debug = True
    app.run(host='0.0.0.0')
