from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open('recetas.json', 'r') as f:
        recetas = json.load(f)
    return render_template('index.html', recetas=recetas)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)