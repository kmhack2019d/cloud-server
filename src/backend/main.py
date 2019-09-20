from flask import Flask, jsonify, render_template
import get_data

app = Flask(__name__, static_folder='static', static_url_path='/', template_folder="static")

@app.route('/api/v1/get_data')
def helloworld():
    data = get_data.getData()
    newest_data = data[0]["data"][0]
    return jsonify(newest_data)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    print (app.url_map)
    app.debug = True
    app.run(host='0.0.0.0')
