## Documentation for VOSK Live Microphone Transcription to Webpage

**This project runs on Python Flask and has a websocket connection. We have a templates folder which contains the index.html file.**

### Overview

This Python script utilizes the VOSK speech recognition library to perform live transcription of audio from your microphone. The transcribed text is then displayed in real-time on a webpage served using Flask and SocketIO. This allows for a dynamic and accessible way to visualize speech-to-text conversion as it happens.

### Features

*   **Live Transcription:**  Continuously transcribes audio input from your microphone.
*   **Webpage Display:** Shows the transcription in real-time within a web browser.
*   **Partial and Full Transcription Updates:**  Provides both intermediate (partial) transcriptions and final (full) transcriptions on the webpage, giving a more fluid user experience.
*   **Vosk Model Integration:** Leverages the accuracy and efficiency of the VOSK offline speech recognition toolkit.
*   **Customizable Input Device:** Allows you to select a specific microphone or audio input device.
*   **Adjustable Sampling Rate:**  Supports specifying the audio sampling rate for optimal performance.
*   **Language Model Selection (Partial):**  The script is set up to use a model named `in_en_model`. While the code has a parameter for language model, it's currently hardcoded to use `in_en_model`.  (Note: The script currently defaults to 'in\_en\_model' and needs modification to fully utilize the `-m` or `--model` argument for different language models.)
*   **Basic Error Logging:** Includes logging for audio stream errors and exceptions to aid in debugging.
*   **Command-line Arguments:** Offers options to configure device, samplerate, language model, host, port, and debug mode.

### Prerequisites

Before running this script, ensure you have the following installed:

1.  **Python 3:**  Python 3.6 or later is required.


### Setup

#### 1. Download VOSK Model

**You have to download the model from this website: [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)**

1.  Visit the VOSK models website linked above.
2.  Select the appropriate model for your desired language. For English transcription, consider `vosk-model-en-us-***` or for Indian English `vosk-model-in-en-0.4`.
3.  Download the ZIP file of the model.
4.  Extract the contents of the downloaded ZIP file to a folder.
5.  **Put the extracted model folder in the root directory of the project.**
6.  **You can either rename the folder or keep the original name and update the `server.py` file accordingly.** By default, the script is configured to look for a model named `in_en_model`. To use the default configuration, **rename the extracted folder to `in_en_model`.**

    The relevant code in `server.py` that loads the model is:

    ```python
    if model_lang is None:
        # Hard coded the in_en_model for now. change it to using model_lang as parameter
        model = Model("in_en_model")
        logger.info("Using default English (US) model")
    else:
        model = Model("in_en_model") # This part needs to be updated to use model_lang
        logger.info(f"Using language model: {model_lang}")
    ```

    If you rename the model folder, ensure the name in the `Model()` function in your `server.py` matches.

#### 2. Create `templates` folder and place `index.html`

1.  In the root directory of your project (where `server.py` will be located), create a folder named `templates`.
2.  You need to create an `index.html` file and place it inside the `templates` folder. This HTML file will serve as the webpage for displaying the live transcription. Create a file named `index.html` and add the necessary HTML structure and Javascript to display the transcription. (See the previous full documentation for the `index.html` code if needed).

    ```
    your_project_directory/  <-- Root directory
    ├── server.py           <-- Your Python script (can be named differently)
    ├── in_en_model/         <-- Renamed VOSK model folder here (or your model folder)
    ├── templates/
    │   └── index.html      <-- index.html inside templates folder
    └── requirements.txt    <-- (Place requirements.txt here)
    ```

#### 3. Set up Virtual Environment

1.  Navigate to your project's root directory in the terminal.
2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    ```
    (This creates a virtual environment named "venv" within your project directory.)
3.  **Activate the virtual environment:**
    *   **On Linux/macOS:**
        ```bash
        source venv/bin/activate
        ```
    *   **On Windows:**
        ```bash
        venv\Scripts\activate
        ```
    (Activating the virtual environment isolates your project's dependencies.)

#### 4. Install Python Dependencies

1.  **After activating the virtual environment**, ensure you are still in your project's root directory.
2.  **Install the required Python libraries from the `requirements.txt` file:**
    ```bash
    pip install -r requirements.txt
    ```
    (This will install libraries like `argparse`, `sounddevice`, `vosk`, `flask`, `flask_socketio` within your virtual environment.)

### Running the Application

1.  Open your terminal or command prompt and navigate to your project's root directory.
2.  **Make sure your virtual environment is activated.**
3.  **Run the project by saying:**
    ```bash
    python server.py
    ```
    (If you named your Python script something other than `server.py`, use that name instead, e.g., `python your_script_name.py`)

4.  You should see output in the terminal indicating the Flask server is running, and potentially messages about the model being loaded and the microphone being accessed.

5.  Open your web browser and go to the address shown in the terminal output (usually something like `http://0.0.0.0:5000/` or `http://127.0.0.1:5000/`).

6.  Allow microphone access if prompted by your browser.

7.  Start speaking into your microphone. You should see the transcription appearing live on the webpage.

### Usage

*   Once the script is running and the webpage is open, simply speak into your microphone.
*   The transcription will appear in the `div` section on the webpage, updating in real-time as you speak.
*   The webpage will display both partial transcriptions (intermediate results) and full transcriptions (more finalized results) as provided by the VOSK model.
*   To stop the transcription, you can interrupt the Python script in your terminal by pressing `Ctrl+C`.

### Command-line Arguments

You can customize the script's behavior using the following command-line arguments when you run it:

*   `-d` or `--device`:  Specify the input device. This can be a numeric ID or a substring of the device name. Use `python server.py -d list` to list available input devices.

    ```bash
    python server.py -d 1  # Use device ID 1
    python server.py -d "microphone" # Use device with "microphone" in its name
    ```

*   `-r` or `--samplerate`:  Specify the sampling rate in Hertz. If not provided, the script will use the default sampling rate of your chosen input device.

    ```bash
    python server.py -r 44100 # Set samplerate to 44100 Hz
    ```

*   `-m` or `--model`:  Specify the language model.  **(Currently, this argument is not fully implemented in the provided script. It is hardcoded to use 'in\_en\_model'.  To use different models, you would need to modify the script to correctly load the model specified by this argument and ensure you place the corresponding model folder in the correct location and potentially rename it if the script expects a specific name).**

    ```bash
    # Example of how it's intended to be used (requires script modification):
    # python server.py -m en-us # Intended to use a model named 'en-us' (requires script modification)
    ```

*   `--host`:  Specify the host address for the Flask application. Defaults to `0.0.0.0` (accessible from any network interface).

    ```bash
    python server.py --host 127.0.0.1 # Only accessible from localhost
    ```

*   `--port`:  Specify the port for the Flask application. Defaults to `5000`.

    ```bash
    python server.py --port 8000 # Run the server on port 8000
    ```

*   `--debug`: Enable debug logging. This will provide more detailed output in the terminal, which can be helpful for troubleshooting.

    ```bash
    python server.py --debug
    ```

### Troubleshooting

*   **"No module named 'vosk'" or similar import errors:** Ensure you have activated your virtual environment and installed the Python requirements correctly using `pip install -r requirements.txt`. Double-check that `vosk` and other libraries are installed in your Python environment.
*   **"Failed to load model" or similar errors:** Verify that you have downloaded the VOSK model, extracted it, and placed the model folder (renamed to `in_en_model` by default) in the root directory of your project. Check for typos in the folder name and in the model name used in `server.py`.
*   **"Audio device error" or no audio input:**
    *   List available audio devices using `python server.py -d list` and check if your microphone is listed.
    *   Ensure your microphone is properly connected and enabled in your operating system's sound settings.
    *   Try specifying a different device ID using the `-d` or `--device` argument.
    *   Check your operating system's permissions to ensure the script has access to your microphone.
*   **Transcription is slow or inaccurate:**
    *   Consider using a different VOSK model. Smaller models might be faster but less accurate. Larger models might be more accurate but slower.
    *   Ensure your audio input is clear and without excessive background noise.
    *   Experiment with different samplerates using the `-r` or `--samplerate` argument.
*   **Webpage not loading or not updating:**
    *   Check the terminal output for any errors from the Flask server or SocketIO.
    *   Ensure your web browser is connected to the internet (though the transcription itself is offline, SocketIO and the webpage require a connection to function correctly locally).
    *   Try clearing your browser cache or opening the webpage in a different browser.
    *   Make sure the Python script is still running in the terminal.

-----
