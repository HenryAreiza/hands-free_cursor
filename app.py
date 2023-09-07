from flask import Flask, render_template, request

app = Flask(__name__)

# Initialize a list to store the points
points = []

@app.route('/')
def index():
    return render_template('index.html', points=points)

@app.route('/add_point', methods=['POST'])
def add_point():
    x = float(request.form['x'])
    y = float(request.form['y'])
    color = request.form['color']
    
    points.append({'x': x, 'y': y, 'color': color})
    
    return 'Point added successfully!'

if __name__ == '__main__':
    app.run(debug=True)
