import gradio as gr
import random
import cv2

# Function to convert a frame to black and white
def black_and_white(frame):
    value  = random.uniform(0,100)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    sentence = f'You owe me {value} dollars'
    return [cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR), sentence]

demo = gr.Interface(
    fn = black_and_white, 
    inputs = gr.Image(source="webcam", streaming=True), 
    outputs = ["image","text"],
    live = True,
    title="You again? come on!, give me a break!",
    description="This app captures your webcam feed and displays it in black and white."
)

demo.launch()