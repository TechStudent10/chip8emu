from display import Display
from cpu import CPU
import pygame

from config import KEYMAP

display = Display(scale=10)
display.init_display()
display.init_keys()
cpu = CPU(display)
cpu.load_sprites_into_mem()
# cpu.load_rom("Space Invaders [David Winter].ch8")
cpu.load_rom("Keypad Test [Hap, 2006].ch8")

while display.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            display.running = False
            break

    cpu.cycle()
