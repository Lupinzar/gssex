# gssex - Genesis Savestate Extractor

A tool for extracting graphics from Sega Genesis (Sega Mega Drive) emulator savestates. Can also be used to search binaries for uncompressed tile graphics. The focus of the tool is graphics ripping rather than debugging. Many emulators provide debugging features, but making use of those modes to produce graphics outputs is lacking or the workflow is very slow. Written in Python with PySide6 (Qt library binding).

## Supported Emulator Savestates

* Genecyst
* Original Gens & KMOD branches
* Gens Rerecording (TAS)
* Kega Fusion
* Exodus (Compressed)

# Using

Check out the Wiki in this repo for a guide on how to use the tool.

# Installing

## Windows

Use the provided pre-built executable in releases.

## Linux / Mac

* Clone this repo or download the source code.
* This project is configured to use uv. This should ensure you have the proper version of python and the needed dependencies. You can find installation instructions here: https://docs.astral.sh/uv/getting-started/installation/
* Use `uv run main.py` to start the application from the gssex directory. On the first run, uv should create a virtual environment with the needed dependencies.
* If you don't want to use uv for some reason, you should still be able to install the dependencies listed in the pyproject.toml file using your preferred method.

# Limitations / Known Issues

The **Screen** mode in the Tile Maps tab is not 100% accurate. Combining the Columm vertical scroll with any Horizontal scrolling may not work. I'm not sure if any commercial games use this combination, but the tool's renderer does not accurately reproduce the strange behavior you get on real hardware or reference emulators. This may be fixed in the future.

All sprites are rendered on the sprite plane under the Sprites tab as long as they are in the linked draw list. There are some special VDP tricks where certain lines of sprites can be blanked out, but this isn't duplicated. You can manually hide those sprites if need be.

The graphics mode for Sega Master System compatibility is not currently supported.

# Libraries Used

* PySide6 (Qt Bindings) - https://doc.qt.io/qt-6/lgpl.html
* Pillow - https://github.com/python-pillow/Pillow/blob/main/LICENSE