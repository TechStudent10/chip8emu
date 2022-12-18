from src.display import Display
from src.cpu import CPU
import argparse, os

parser = argparse.ArgumentParser(
    prog="CHIP-8 Emulator",
    description="A basic CHIP-8 emulator written in Python"
)

parser.add_argument("rom_name")
parser.add_argument("-d", "--debug", action="store_true", default=False)
parser.add_argument("--scale", type=int, required=False, default=10)

args = parser.parse_args()

display = Display(scale=args.scale)
display.init_display()
display.init_keys()
cpu = CPU(display, args.debug)
cpu.load_sprites_into_mem()
cpu.load_rom(os.path.join("roms", args.rom_name))

while cpu.running:
    cpu.cycle()
