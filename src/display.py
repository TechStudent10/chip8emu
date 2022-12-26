from .config import WIDTH, HEIGHT, KEYMAP, KEYREF, KEYLOOKUP, INVERTED_KEYMAP
import pygame, math
pygame.init()

class Display:
    def __init__(self, width=None, height=None, scale=None):
        self.width = width or WIDTH
        self.height = height or HEIGHT
        self.scale = scale or 1
        self.screen = None
        self.pixels = []
        self.keys_pressed = {}
        self.on_next_key_press = None

    def init_display(self):
        self.screen = pygame.display.set_mode((self.width*self.scale, self.height*self.scale))
        pygame.display.set_caption("Chip-8 Emulator")

    def init_keys(self):
        for key in KEYMAP:
            self.keys_pressed[key] = False

    def get_pg_key(self, keycode):
        pg_key = None
        try:
            pg_key = KEYREF[keycode]
        except KeyError:
            pass

        return pg_key

    def get_keycode(self, pg_key):
        keycode = INVERTED_KEYMAP[KEYMAP[pg_key]]
        return keycode

    def get_pressed(self):
        return pygame.key.get_pressed()

    def is_pressed(self, key):
        return self.get_pg_key(key) in self.keys_pressed

    def on_key_down(self, key):
        self.keys_pressed[key] = True

        if self.on_next_key_press != None and key:
            self.on_next_key_press(key)
            self.on_next_key_press = None

    def on_key_up(self, key):
        self.keys_pressed[key] = False

    def draw_pixel(self, x, y):
        if x > self.width:
            x -= self.width
        elif x < 0:
            x += self.width

        if y > self.height:
            x -= self.height
        elif x < 0:
            x += self.height
        
        self.pixels.append((x, y))

        return not self.pixels[len(self.pixels) - 1]

    def clear_display(self):
        self.pixels = []

    def render(self):
        self.screen.fill((0,0,0))

        for i in range(len(self.pixels)):
            pixel = self.pixels[i]
            x = pixel[0]
            y = pixel[1]

            pygame.draw.rect(self.screen, (255,255,255), (
                x * self.scale, y * self.scale, self.scale, self.scale)
            )

        pygame.display.update()
