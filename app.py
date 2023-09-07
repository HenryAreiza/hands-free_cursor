from flask import Flask, render_template
import random

app = Flask(__name__)

canvas_data = {
    "x": 0.0,
    "y": 0.0,
    "color": "black",
}


@app.route('/')
def index():
    return render_template('index.html', canvas_data=canvas_data)


@app.route('/demo')
def demo():
    x = random.uniform(0, 1)
    y = random.uniform(0, 1)
    colors = ["red", "green", "blue", "orange", "purple"]
    color = random.choice(colors)

    draw_point(x, y, color)
    
    return ""


def draw_point(x, y, color):
    canvas_data["x"] = x
    canvas_data["y"] = y
    canvas_data["color"] = color


if __name__ == '__main__':
    app.run(debug=True)
