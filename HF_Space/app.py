import gradio as gr
from FacePosition import FacePosition
from AudioClassifier import AudioClassifier


# Create an instance of the FacePosition class
movement_controller = FacePosition()

cursor_movement = gr.Interface(
    fn = movement_controller.predict, 
    inputs = gr.Image(source='webcam', streaming=True), 
    outputs = ['image', 'text'],
    live = True,
    title = 'Cursor movement controller',
    description = "This space provides functionality for detecting a face using the MediaPipe library and controlling the cursor's movement accordingly."
)


# Create an instance of the AudioClassifier class
audio_classifier = AudioClassifier()

audio_commands = gr.Interface(
    fn = audio_classifier.predict,
    inputs = gr.Audio(source="microphone", type="filepath", streaming=True),
    outputs = "text",
    live = True,
    title = 'Speech commands recognition (mouse actions)',
    description = 'This class provides functionality for classifying audio commands associated to mouse actions, based on a pre-trained audio classification model.'
    )


demo = gr.TabbedInterface([cursor_movement, audio_commands],
                          title = 'Hands-free Cursor Application',
                          tab_names = ['Cursor movement controller', 'Speech commands recognition'],
                          theme = gr.themes.Soft())


if __name__ == "__main__":
    demo.launch()
