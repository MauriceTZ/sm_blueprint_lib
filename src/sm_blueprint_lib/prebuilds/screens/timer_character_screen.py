import os
from numpy import ndarray, array, flip
import pygame as pg

from ...constants import TICKS_PER_SECOND

from ...prebuilds import timer_ram_multiclient

from ...utils import get_bits_required, connect, mask
from ...blueprint import Blueprint
from ...parts import LogicGate
from ...parts import Timer
from ...pos import *
from ..decoder import decoder


def timer_character_screen(bp: Blueprint, ncols: int, nrows: int, do_preview: bool = False, pos: Pos | Sequence = (0, 0, 0)):
    pos = check_pos(pos)
    num_chars = ncols * nrows
    timer_ram = timer_ram_multiclient(
        bp, bit_length=5*8, num_address=num_chars, num_clients=1, pos=pos)
    pg.font.init()
    path_font = os.path.join(os.path.dirname(
        os.path.abspath(__file__)),  "lcd_font.ttf")
    timer_font = pg.font.Font(path_font, 100)
    printable_char_size = (max(timer_font.size(chr(n))[0] for n in range(255)),
                           max(timer_font.size(chr(n))[1] for n in range(255)))
    timer_screen = ndarray((ncols, nrows, 5, 8, 2), dtype=object)
    timer_write_enable = ndarray((ncols * nrows), dtype=object)
    for x in range(ncols):
        for y in range(nrows):
            timer_write_enable[x + y * ncols] = LogicGate(
                pos + (11*x, 0, 2+9*y), "FF0000")
            for charx in range(5):
                for chary in range(8):
                    timer_screen[x, y, charx, chary, :] = (
                        LogicGate(pos + (2*charx+11*x, 1,
                                  chary+2+9*y), "000000"),
                        Timer(pos + (2*charx+11*x, 2, 1+chary+2+9*y),
                              "000000", divmod(num_chars, TICKS_PER_SECOND),
                              xaxis=-3, zaxis=-2)
                    )
                    connect(timer_write_enable[x + y * ncols],
                            timer_screen[x, y, charx, chary, 0])
                    connect(timer_screen[x, y, charx, chary, 0],
                            timer_screen[x, y, charx, chary, 1])
            connect(timer_ram[1][:, 0],
                    timer_screen[x, y, :, :, 0].flatten(order="F"))
    dec = decoder(bp, num_chars, pos + (-1, 2, 1),
                  with_enable=False, precreated_outputs=timer_write_enable)
    clock_buffer = [LogicGate(pos + (5*8+x, 0, 1), "000000", 1)
                    for x in range(get_bits_required(num_chars))]
    connect(timer_ram[0][:, 0], clock_buffer)
    connect(clock_buffer, dec[0])
    char_input = array([
        (LogicGate(pos + (x, 13, 0), "FF0000", 4),
         LogicGate(pos + (x, 14, 0), "FF0000", 1))
        for x in range(8)
    ], dtype=object)
    char_decoder = []
    pg.init()
    for nchar in range(256):
        try:
            surface = timer_font.render(chr(nchar), False, (255, 255, 255))
        except (ValueError, pg.error):
            continue
        if surface.get_size() != printable_char_size:
            continue
        surface = pg.transform.flip(surface, False, True)
        a = printable_char_size[0] * (1/6)
        b = printable_char_size[1] * (1/10)
        x0 = 0
        y0 = b
        x1 = printable_char_size[0] - a
        y1 = printable_char_size[1] - b*2
        surface = surface.convert(32, 0)
        surface = pg.Surface.subsurface(surface, (x0, y0, x1, y1))
        surface = pg.transform.smoothscale(surface, (5, 8))
        surface_array = pg.surfarray.pixels2d(surface)
        surface_array[surface_array > 0] = 1
        surface_array = flip(surface_array, 0)
        if surface_array.any():
            char_decoder.append(g0 := LogicGate(
                pos + (len(char_decoder) % (5*8), 12-len(char_decoder)//(5*8), 0), "000000"))
            connect(mask(char_input[:, 0], ~nchar, 8), g0)
            connect(mask(char_input[:, 1], nchar, 8), g0)
            for x in range(5):
                for y in range(8):
                    if surface_array[x, y] == 1:
                        connect(g0, timer_ram[3][0][7][0][x+5*y, 3])

    if do_preview:
        id_font = pg.font.Font(None, 25)
        pg.key.set_repeat(100)
        win_size = ((printable_char_size[0] + 1) * ncols,
                    (printable_char_size[1] + 1) * nrows)
        window = pg.display.set_mode(win_size)
        pg.display.set_caption("test")
        clock = pg.time.Clock()
        running = True
        start_char = 32
        while running:
            window.fill((0, 0, 0))
            for n in range(nrows * ncols):
                id_chr = n+start_char
                surface_id = id_font.render(
                    f"ID: {id_chr}", True, (255, 255, 255))
                try:
                    surface = timer_font.render(
                        chr(id_chr), False, 0x3d8f9a, 0x1b1b21)
                    a = printable_char_size[0] * (1/6)
                    charx = printable_char_size[1] * (1/10)
                    x0 = 0
                    y0 = charx
                    x1 = printable_char_size[0] - a
                    y1 = printable_char_size[1] - charx*2
                    surface = surface.convert()
                    surface = pg.Surface.subsurface(surface, (x0, y0, x1, y1))
                    surface = pg.transform.smoothscale(surface, (5, 8))
                    surface = pg.transform.scale(surface, printable_char_size)
                    window.blit(
                        surface,
                        ((printable_char_size[0]+1) * (n % ncols),
                            (printable_char_size[1]+1) * (n // ncols))
                    )
                except Exception:
                    pass
                window.blit(
                    surface_id, ((printable_char_size[0]+1) * (n % ncols),
                                 (printable_char_size[1]+1) * (n // ncols)))
            pg.display.flip()
            clock.tick(30)
            for event in pg.event.get():
                match event.type:
                    case pg.QUIT:
                        running = False
                        break
                    case pg.KEYDOWN:
                        if event.key == pg.K_RIGHT:
                            start_char += 1
                        elif event.key == pg.K_LEFT:
                            start_char -= 1

    bp.add(timer_write_enable, timer_screen,
           clock_buffer, char_input, char_decoder)
