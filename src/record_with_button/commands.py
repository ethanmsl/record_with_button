"""
*De facto* `main`, holding the key functions acting as entry points
to any other code and acting as the bridge to the user via
the typer framework and decorators.
"""

import time
import tkinter as tk
from importlib import metadata
from typing import Optional

import numpy as np
import sounddevice as sd
import typer
import wavio
from rich import print as rprint
from rich.progress import Progress, SpinnerColumn, TextColumn, track
from typing_extensions import Annotated

from . import __name__ as APP_NAME

# generage CLI app object
app = typer.Typer(rich_markup_mode="rich", add_completion=False)

# get version from pyproject.toml
__version__ = metadata.version(__package__)

##################################################################################
# Boilerplate
##################################################################################


def version_callback(version: bool):
    """
    Print app version and exit
    """
    if version:
        rprint(f"record_with_button ('{APP_NAME}') Version: {__version__}")
        raise typer.Exit()


@app.callback(help="[bold]record_with_button[/bold] CLI App")
def app_options(
    _: bool = typer.Option(
        None,
        "--version",
        help="Show version of this app",
        callback=version_callback,
        is_eager=True,
    )
):
    """
    This callback is called by the **base app** itself.
    Sub-callbacks are used by the options to perform actions.
    The eager sub-callback allows us to circumvent typer's expectation that a regular
    command is still comming.

    (Side Note: Yes, I agree this is slightly awkward for something as standard as
    `--version`, but it does seem to be the best way to do it in this framework.)
    """


##################################################################################
# Regular 'ol Commands
##################################################################################


@app.command()
def info(more: Annotated[bool, typer.Option(help="more info")] = False) -> None:
    """Just for me as I figure out how these libraries work and the info they need."""
    max_channels = sd.query_devices(kind="input")["max_input_channels"]
    print(f"Max Channels: {max_channels}")
    if more:
        for elem in sd.query_devices(kind="input"):
            print(f"Buncha stuff: {elem}")


@app.command(rich_help_panel="Record")
def record_audio_until_button_pushed():
    """
    Records audio to a wav file at proj directory root.
    File is labelled "*recording.wave*"
    Re-recording will overwrite the previous file.
    """
    # Parameters for recording
    RATE = 44100  # Sample rate  # pylint: disable=invalid-name
    CHANNELS = (
        1  # Number of channels (1=mono, 2=stereo)  # pylint: disable=invalid-name
    )
    DTYPE = np.int16  # Data type
    # CHUNK_SIZE = 1024  # Number of frames per buffer  # pylint: disable=invalid-name
    RECORDING = True  # pylint: disable=invalid-name

    # Create a buffer to store audio data
    audio_buffer = np.empty((0, CHANNELS), dtype=DTYPE)

    # Callback function for the audio stream
    def audio_callback(indata, frames, time, status):  # pylint: disable=all
        """Passed to sounddevice 'stream'; records"""
        nonlocal audio_buffer
        audio_buffer = np.append(audio_buffer, indata, axis=0)

    # Start the audio stream
    stream = sd.InputStream(
        samplerate=RATE, channels=CHANNELS, dtype=DTYPE, callback=audio_callback
    )
    stream.start()

    # Function to stop recording when button is pushed
    def stop_recording():
        """pasesed to tkinter button; ends recording"""
        nonlocal RECORDING
        RECORDING = False  # pylint: disable=invalid-name
        stream.stop()
        stream.close()
        if audio_buffer.size > 0:  # Check if there's any recorded data
            wavio.write("recording.wav", audio_buffer, RATE, sampwidth=2)
        root.quit()

    # Create a simple GUI window with a button
    root = tk.Tk()
    root.title("Audio Recorder")
    button = tk.Button(root, text="Stop Recording", command=stop_recording)
    button.pack(pady=20)
    root.mainloop()
