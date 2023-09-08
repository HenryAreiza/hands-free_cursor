from flask import Flask, render_template
import gradio as gr

app = Flask(__name__)

# Initialize an empty list to store the points
points = []

# Define a Gradio interface to capture the point coordinates and color
def draw_point(x: float, y: float, color: str):
    # Add the point to the list
    points.append((x, y, color))
    return "Point added successfully!"

# Define a Gradio interface to display the canvas and point inputs
canvas_interface = gr.Interface(
    fn=draw_point,
    inputs=[
        gr.inputs.Number(label="X Coordinate (0 to 1)"),
        gr.inputs.Number(label="Y Coordinate (0 to 1)"),
        gr.inputs.Textbox(label="Color (e.g., 'red')"),
    ],
    outputs=gr.outputs.Textbox(),
    live=True,
)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Start the Gradio interface in a separate thread
    canvas_interface.launch(share=True)
    # Run the Flask app
    app.run(debug=True)
