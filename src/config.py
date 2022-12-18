import pygame

WIDTH = 64
HEIGHT = 32

PC_START = 0x200

KEYMAP = {
    pygame.K_1: 0x1, # 1
    pygame.K_2: 0x2, # 2
    pygame.K_3: 0x3, # 3
    pygame.K_4: 0xc, # 4
    pygame.K_q: 0x4, # Q
    pygame.K_w: 0x5, # W
    pygame.K_e: 0x6, # E
    pygame.K_r: 0xD, # R
    pygame.K_a: 0x7, # A
    pygame.K_s: 0x8, # S
    pygame.K_d: 0x9, # D
    pygame.K_f: 0xE, # F
    pygame.K_z: 0xA, # Z
    pygame.K_x: 0x0, # X
    pygame.K_c: 0xB, # C
    pygame.K_v: 0xF  # V
}

INVERTED_KEYMAP = {
    0x1: pygame.K_1, # 1
    0x2: pygame.K_2, # 2
    0x3: pygame.K_3, # 3
    0xc: pygame.K_4, # 4
    0x4: pygame.K_q, # Q
    0x5: pygame.K_w, # W
    0x6: pygame.K_e, # E
    0xD: pygame.K_r, # R
    0x7: pygame.K_a, # A
    0x8: pygame.K_s, # S
    0x9: pygame.K_d, # D
    0xE: pygame.K_f, # F
    0xA: pygame.K_z, # Z
    0x0: pygame.K_x, # X
    0xB: pygame.K_c, # C
    0xF: pygame.K_v  # V
}

# Key reference
KEYREF = {
    49: pygame.K_1, # 1
    50: pygame.K_2, # 2
    51: pygame.K_3, # 3
    52: pygame.K_4, # 4
    81: pygame.K_q, # Q
    87: pygame.K_w, # W
    69: pygame.K_e, # E
    82: pygame.K_r, # R
    65: pygame.K_a, # A
    83: pygame.K_s, # S
    68: pygame.K_d, # D
    70: pygame.K_f, # F
    90: pygame.K_z, # Z
    88: pygame.K_x, # X
    67: pygame.K_c, # C
    86: pygame.K_v  # V
}

# Key lookup
KEYLOOKUP = {
    49: 0x1, # 1
    50: 0x2, # 2
    51: 0x3, # 3
    52: 0xc, # 4
    81: 0x4, # Q
    87: 0x5, # W
    69: 0x6, # E
    82: 0xD, # R
    65: 0x7, # A
    83: 0x8, # S
    68: 0x9, # D
    70: 0xE, # F
    90: 0xA, # Z
    88: 0x0, # X
    67: 0xB, # C
    86: 0xF  # V
}
