# (Very Buggy) Python CHIP-8 Emulator

Made in a weekend!

## Usage

> Note: Make sure all your ROMs are in the `roms/` directory. The emulator will read directly from there.

Help message from `emu.py`

```
usage: CHIP-8 Emulator [-h] [-d] [--scale SCALE] rom_name

A basic CHIP-8 emulator written in Python

positional arguments:
  rom_name

options:
  -h, --help     show this help message and exit
  -d, --debug
  --scale SCALE
```

## Example

```
python emu.py --scale 20 "IBM Logo.ch8"
```

## Installation

```
pip install -r requirements.txt
```
