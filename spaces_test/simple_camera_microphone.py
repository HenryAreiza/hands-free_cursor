import gradio as gr
import cv2
import random
from transformers import pipeline
import time

#%% SIMPLE CAMERA
#################
# Function to convert a frame to black and white
def black_and_white(frame):
    value  = random.uniform(0,100)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    sentence = f'You owe me {value} dollars'
    return [cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR), sentence]

simple_camera = gr.Interface(
    fn = black_and_white, 
    inputs = gr.Image(source="webcam", streaming=True), 
    outputs = ["image","text"],
    live = True,
    title="You again? come on!, give me a break!",
    description="This app captures your webcam feed and displays it in black and white."
)

#%% SIMPLE MICROPHONE
#####################

p = pipeline("automatic-speech-recognition")

def transcribe(audio):
    time.sleep(1)
    text = p(audio)["text"]
    return text

simple_microphone = gr.Interface(
    fn=transcribe,
    inputs = gr.Audio(source="microphone",type="filepath",streaming=True),
    outputs= "textbox",
    live=True,
    title="You again? come on!, give me a break!",
    description="This app captures your microphone to predict what you are saying."
    )

demo = gr.TabbedInterface([simple_camera, simple_microphone])

if __name__ == "__main__":
    demo.launch()
