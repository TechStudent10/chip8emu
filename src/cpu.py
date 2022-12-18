from .config import PC_START, KEYMAP
import random, math, pygame

from collections import deque

class CPU():
    """
    This is the CPU class for the CHIP-8 emulator
    """
    def __init__(self, display):
        self.display = display

        self.memory = bytearray(4096)

        # Timers
        self.sound_timer = 0
        self.delay_timer = 0

        # Registers
        self.v = [0] * 16
        self.i = 0
        self.pc = PC_START
        self.stack = deque()

        self.speed = 10
        self.paused = False

        self.running = True

        self.clock = pygame.time.Clock()

    def load_sprites_into_mem(self):
        sprites = [
            0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
            0x20, 0x60, 0x20, 0x20, 0x70, # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
            0x90, 0x90, 0xF0, 0x10, 0x10, # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
            0xF0, 0x10, 0x20, 0x40, 0x40, # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90, # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
            0xF0, 0x80, 0x80, 0x80, 0xF0, # C
            0xE0, 0x90, 0x90, 0x90, 0xE0, # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
            0xF0, 0x80, 0xF0, 0x80, 0x80  # F
        ]

        for i in range(len(sprites)):
            self.memory[i] = sprites[i]

    def load_prog_into_mem(self, program):
        for index, val in enumerate(program):
            self.memory[PC_START + index] = val

    def cycle(self):
        if self.running:
            # Comment out this part if you aren't using Pygame
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in KEYMAP:
                        self.display.on_key_down(event.key)
                if event.type == pygame.KEYUP:
                    if event.key in KEYMAP:
                        self.display.on_key_up(event.key)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False # Make sure you call this somewhere to stop the emulator
        
            for i in range(self.speed):
                if not self.paused:
                    opcode = (self.memory[self.pc] << 8 | self.memory[self.pc + 1])
                    self.execute_instruction(opcode)

            if not self.paused:
                self.update_timers()
            
            self.display.render()

                # print(self.paused)

    def update_timers(self):
        if self.delay_timer > 0:
            self.delay_timer -= 1

        if self.sound_timer > 0:
            self.sound_timer -= 1

    def load_rom(self, filename):
        rom = open(filename, 'rb')
        romdata = rom.read()
        rom.close()

        self.load_prog_into_mem(romdata)

    def execute_instruction(self, opcode):
        self.pc += 2
        self.x = ((opcode & 0x0F00) >> 8) & 0xF
        self.y = ((opcode & 0x00F0) >> 4) & 0xF
        self.opcode = opcode
        # print(self.opcode)

        match (opcode & 0xF000):
            case 0x0000:
                match (opcode):
                    case 0x00E0:
                        self.cls()
                    case 0x00EE:
                        self.ret()
            case 0x1000:
                self.jp_appr()
            case 0x2000:
                self.call_addr()
            case 0x3000:
                self.se_vx()
            case 0x4000:
                self.sne_Vx()
            case 0x5000:
                self.se_vx_vy()
            case 0x6000:
                self.ld_vx()
            case 0x7000:
                self.add_vx()
            case 0x8000:
                match (opcode & 0xF):
                    case 0x0:
                        self.ld_vx_vy()
                    case 0x1:
                        self.or_vx_vy()
                    case 0x2:
                        self.and_vx_vy()
                    case 0x3:
                        self.xor_vx_vy()
                    case 0x4:
                        self.add_vx_vy()
                    case 0x5:
                        self.sub_vx_vy()
                    case 0x6:
                        self.shr_vx()
                    case 0x7:
                        self.subn_vx_vy()
                    case 0xE:
                        self.shl_vx()
            case 0x9000:
                self.sne_vx_vy()
            case 0xA000:
                self.LD_I_addr()
            case 0xB000:
                self.jp_v0_addr()
            case 0xC000:
                self.rnd_vx()
            case 0xD000:
                self.drw_vx_vy()
            case 0xE000:
                match (opcode & 0xFF):
                    case 0x9E:
                        self.skp_vx()
                    case 0xA1:
                        self.sknp_vx()
            case 0xF000:
                match (opcode & 0xFF):
                    case 0x07:
                        self.ld_vx_dt()
                    case 0x0A:
                        self.ld_vx_paused()
                    case 0x15:
                        self.ld_dt_vx()
                    case 0x18:
                        self.ld_st_vx()
                    case 0x1E:
                        self.add_i_vx()
                    case 0x29:
                        self.ld_f_vx()
                    case 0x33:
                        self.ld_b_vx()
                    case 0x55:
                        self.ld_i_vx()
                    case 0x65:
                        self.ld_vx_i()

    def cls(self):
        self.display.clear_display()

    def ret(self):
        self.pc = self.stack.pop()

    def jp_appr(self):
        self.pc = (self.opcode & 0xFFF)

    def call_addr(self):
        self.stack.append(self.pc)
        self.pc = (self.opcode & 0xFFF)

    def se_vx(self):
        if self.v[self.x] == (self.opcode & 0xFF):
            self.pc += 2

    def sne_Vx(self):
        if self.v[self.x] != (self.opcode & 0xFF):
            self.pc += 2

    def se_vx_vy(self):
        if self.v[self.x] == self.v[self.y]:
            self.pc += 2

    def ld_vx(self):
        self.v[self.x] = (self.opcode & 0xFF)

    def add_vx(self):
        self.v[self.x] = self.v[self.x] + (self.opcode & 0xFF)

    def ld_vx_vy(self):
        self.v[self.x] = self.v[self.y]

    def or_vx_vy(self):
        # note, may cause issues
        self.v[self.x] = self.v[self.y] or self.v[self.x]

    def and_vx_vy(self):
        # note, may cause issues
        self.v[self.x] = self.v[self.x] and self.v[self.y]

    def xor_vx_vy(self):
        self.v[self.x] = self.v[self.x] ^ self.v[self.y]

    def add_vx_vy(self):
        sum = self.v[self.x] + self.v[self.y]

        self.v[0xF] = 0

        if sum > 0xFF:
            self.v[0xF] = 1

        self.v[self.x] = sum

    def sub_vx_vy(self):
        self.v[0xF] = 0
        if self.v[self.x] > self.v[self.y]:
            self.v[0xF] = 1

    def shr_vx(self):
        self.v[0xF] = self.v[self.x] & 0x1

        self.v[self.x] = self.v[self.x] >> 1

    def subn_vx_vy(self):
        self.v[0xF] = 0
        if self.v[self.y] > self.v[self.x]:
            self.v[0xF] = 1

        self.v[self.x] = self.v[self.y] - self.v[self.x]

    def shl_vx(self):
        self.v[0xF] = self.v[self.x] & 0x80
        self.v[self.x] = self.v[self.x] << 1

    def sne_vx_vy(self):
        if self.v[self.x] != self.v[self.y]:
            self.pc += 2

    def LD_I_addr(self):
        self.i = self.opcode & 0xFFF

    def jp_v0_addr(self):
        self.pc = (self.opcode & 0xFFF) + self.v[0]

    def rnd_vx(self):
        rand = math.floor(random.randint(0, 255) * 0xFF)
        self.v[self.x] = rand & (self.opcode & 0xFF)

    def drw_vx_vy(self):
        width = 8
        height = self.opcode & 0x000F

        self.v[0xF] = 0

        for row in range(height):
            sprite = self.memory[self.i + row]

            for col in range(width):
                if (sprite & 0x80) > 0:
                    if self.display.draw_pixel(self.v[self.x] + col, self.v[self.y] + row):
                        self.v[0xF] = 1

                sprite = sprite << 1

    def skp_vx(self):
        if self.display.is_key_pressed(self.v[self.x]):
            self.pc += 2

    def sknp_vx(self):
        if not self.display.is_pressed(self.v[self.x]):
            self.pc += 2

    def ld_vx_dt(self):
        self.v[self.x] = self.delay_timer

    def ld_vx_paused(self):
        self.paused = True

        def onNextKeyPress(key):
            self.v[self.x] = key
            self.paused = False
        
        self.display.on_next_key_press = onNextKeyPress

    def ld_dt_vx(self):
        self.delay_timer = self.v[self.x]

    def ld_st_vx(self):
        self.sound_timer = self.v[self.x]

    def add_i_vx(self):
        self.i += self.v[self.x]

    def ld_f_vx(self):
        self.i = self.v[self.x] * 5

    def ld_b_vx(self):
        self.memory[self.i] = int(self.v[self.x] / 100)

        self.memory[self.i + 1] = int((self.v[self.x] % 100) / 10)

        self.memory[self.i + 2] = int(self.v[self.x] % 10)

    def ld_i_vx(self):
        for reg_index in range(self.x):
            print(self.i + reg_index)
            self.memory[self.i + reg_index] = self.v[reg_index]

    def ld_vx_i(self):
        for reg_index in range(self.x):
            self.v[reg_index] = self.memory[self.i + reg_index]