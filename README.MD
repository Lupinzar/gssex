# gssex - Genesis Savestate Extractor

A tool for extracting graphics from Genesis emulator savestates. Can also be used to search binaries for uncompressed tile graphics. The focus of the tool is graphics ripping rather than debugging. Many emulators provide debugging features, but making use of those modes to produce graphics outputs is lacking or the workflow is very slow. Written in Python with PySide6 (Qt library binding).

## Supported Emulator Savestates

* Genecyst
* Original Gens & KMOD branches
* Gens Rerecording (TAS)
* Kega Fusion

# Using

Check out the Wiki in this repo for a guide on how to use the tool.

# Installing

## Windows

Use the provided pyinstaller built executable in releases.

## Linux / Mac

* Clone this repo or download the source code.
* Make sure you have Python installed. I recommened using an virtual environment. The application was designed for Python 3.13. It may work on earlier releases, but there are no guarantees.
* Use pip to install the required dependencies. `pip install -r requirements.txt`
* Run the `main.py` script with your python interpreter.

# Limitations / Known Issues

The **Screen** mode in the Tile Maps tab is not 100% accurate. Combining the Columm vertical scroll with any Horizontal scrolling may not work. I'm not sure if any commercial games use this combination, but the tool's renderer does not accurately reproduce the strange behavior you get on real hardware or reference emulators. This may be fixed in the future.

All sprites are rendered on the sprite plane under the Sprites tab as long as they are in the linked draw list. There are some special VDP tricks where certain lines of sprites can be blanked out, but this isn't duplicated. You can manually hide those sprites if need be.