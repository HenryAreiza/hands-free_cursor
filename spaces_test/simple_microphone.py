from transformers import pipeline
import gradio as gr
import time

p = pipeline("automatic-speech-recognition")

def transcribe(audio):
    time.sleep(1)
    text = p(audio)["text"]
    return text

demo = gr.Interface(
    fn=transcribe,
    inputs = gr.Audio(source="microphone",type="filepath",streaming=True),
    outputs= "textbox",
    live=True)

demo.launch()