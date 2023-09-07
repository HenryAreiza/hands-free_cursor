from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Initialize variables to store the last values
last_x = 0.0
last_y = 0.0
last_color = ""

@app.route('/')
def index():
    return render_template('index.html', last_x=last_x, last_y=last_y, last_color=last_color)

@app.route('/draw_point', methods=['POST'])
def draw_point():
    global last_x, last_y, last_color

    # Get data from the request
    data = request.get_json()
    x = float(data['x'])
    y = float(data['y'])
    color = data['color']

    # Update the last values
    last_x = x
    last_y = y
    last_color = color

    return jsonify({'message': 'Point drawn successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
