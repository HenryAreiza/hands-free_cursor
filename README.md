<p align="center">
    <a href="VERSION" alt="version">
        <img src="https://img.shields.io/badge/version-0.0.0-lightgray" /></a>    
    <a href="LICENSE" alt="License">
        <img src="https://img.shields.io/badge/license-Apache_2.0-blue" /></a>
    <a href="PLATFORM" alt="Platform">
        <img src="https://img.shields.io/badge/platform-linux--64,_macOS,_windows-red" /></a>  
    <a href="CONTRIBUTORS" alt="Contributors">
        <img src="https://img.shields.io/badge/contributors-2-brightgreen" /></a>                
</p>

# Hands-free Cursor Application

This GitHub repository represents a comprehensive application for controlling the computer's cursor and performing various mouse actions using voice commands and head position. This application is designed to provide hands-free control and enhance accessibility for users with motor disabilities. It integrates three major components: audio classification, face detection for cursor positioning, and mouse action execution.


## Table of Contents

- [Hands-free Cursor Application](#hands-free-cursor-application)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
    - [Voice Commands](#voice-commands)
    - [Movement control](#movement-control)
    - [Running the Application](#running-the-application)
    - [Testing Individual Components](#testing-individual-components)
  - [HuggingFace space](#huggingface-space)
  - [Authors](#authors)
  - [License](#license)

## Getting Started

Follow these instructions to get the Hands-free Cursor Application up and running on your local machine.

### Prerequisites

Before you begin, ensure you have met the following requirements:

- [Python 3.10.4](https://www.python.org/downloads/release/python-3104/) or higher installed.
- [virtualenv](https://virtualenv.pypa.io/en/latest/) installed (for creating a virtual environment).

### Installation

1. Clone the repository to your local machine:
```bash
git clone https://github.com/HenryAreiza/hands-free_cursor.git
```

2. Navigate to the project directory:
```bash
cd hands-free_cursor
```

3. Create a virtual environment (recommended):
```bash
virtualenv venv
```

4. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- macOS and Linux:
```bash
source venv/bin/activate
```

5. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Voice Commands
Here are the available voice commands and their corresponding actions:
- **"left"**: Performs a left mouse click.
- **"right"**: Performs a right mouse click.
- **"up"** or **"down"**: Scrolls the mouse wheel up or down, respectively.
- **"go"**: Performs a double left mouse click.
- **"follow"**: Initiates a sustained left mouse click (release by - repeating the command).
- **"on"**: Activates the functionality for cursor movement controlled by head position.
- **"off"**: Deactivates the functionality for cursor movement controlled by head position.
- **"one"**, **"two"**, **"three"**: Adjusts the cursor speed (and scroll step) to slow, medium, or fast, respectively.
- **"stop"**: Exits the program and terminates the application.

### Movement control
You can control the cursor movement with slight movements of your head in an intuitive way. The following images represent the different movements that the model can recognize:

| <img src="media/0.jpg" alt="Center" width="200" height="210"> | <img src="media/1.jpg" alt="Up" width="200" height="210"> | <img src="media/8.jpg" alt="Left/Up" width="200" height="210"> |
|:--:|:--:|:--:|
| *Center* | *Up* | *Left/Up* |

| <img src="media/7.jpg" alt="Left" width="200" height="210"> | <img src="media/6.jpg" alt="Left/Down" width="200" height="210"> | <img src="media/5.jpg" alt="Down" width="200" height="210"> |
|:--:|:--:|:--:|
| *Left* | *Left/Down* | *Down* |

| <img src="media/4.jpg" alt="Right/Down" width="200" height="210"> | <img src="media/3.jpg" alt="Right" width="200" height="210"> | <img src="media/2.jpg" alt="Right/Up" width="200" height="210"> |
|:--:|:--:|:--:|
| *Right/Down* | *Right* | *Right/Up* |



### Running the Application
To start the Hands-free Cursor Application, run the following command:
```bash
python main.py
```
- This will initiate the application, allowing you to control the cursor and perform mouse actions using voice commands and head position.

- Follow the voice command instructions provided in the application. You can move your head to control the cursor intuitively.

- To exit the application, issue the "stop" voice command or close the application window.

You can also configure the application to not display on-screen messages during execution using the ```--verbose``` parameter, as well as control the sensitivity of the microphone to recognize voice commands with the ```--mic_sens``` parameter.

```bash
python main.py --verbose 0 --mic_sens 0.7
```

### Testing Individual Components
You can test individual components of the application by running the following scripts:

- **Audio Classifier:**
This script allows you to test the audio classification component independently.
```bash
python src/AudioClassifier.py
```

- **Face Position Controller:**
This script lets you test the face detection and cursor positioning component separately.
```bash
python src/FacePosition.py
```

## HuggingFace space

In case you want to test the AI models used in this project, without having to install anything on your machine, you can take a look at the [HuggingFace Space](https://huggingface.co/spaces/HenRick69/Hands-free_Cursor) created for this purpose.

## Authors
- [HenryAreiza](https://github.com/HenryAreiza)
- [deividbotina-alv](https://github.com/deividbotina-alv)

## License
This project is licensed under the Apache License Version 2.0 - see the LICENSE file for details.






