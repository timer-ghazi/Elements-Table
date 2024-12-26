#!/usr/bin/env python3
import curses
import sys
from elements_table import Elements

###############################################################################
# BOX-DRAWING CHARACTERS
###############################################################################
BOX_CHARS = {
    "ul": "┌",
    "ur": "┐",
    "ll": "└",
    "lr": "┘",
    "h":  "─",
    "v":  "│"
}

###############################################################################
# TABLE LAYOUT
###############################################################################
TABLE_POSITIONS = {
    (0, 0): "H",  (0, 17): "He",

    (1, 0): "Li", (1, 1): "Be",          (1, 12): "B", (1, 13): "C",
    (1, 14): "N", (1, 15): "O", (1, 16): "F", (1, 17): "Ne",

    (2, 0): "Na", (2, 1): "Mg",          (2, 12): "Al", (2, 13): "Si",
    (2, 14): "P", (2, 15): "S", (2, 16): "Cl", (2, 17): "Ar",

    (3, 0): "K",  (3, 1): "Ca", (3, 2): "Sc", (3, 3): "Ti", (3, 4): "V",
                  (3, 5): "Cr", (3, 6): "Mn", (3, 7): "Fe", (3, 8): "Co",
                  (3, 9): "Ni", (3,10): "Cu", (3,11): "Zn",
                  (3,12): "Ga", (3,13): "Ge", (3,14): "As", (3,15): "Se",
                  (3,16): "Br", (3,17): "Kr",

    (4, 0): "Rb", (4, 1): "Sr", (4, 2): "Y",  (4, 3): "Zr", (4, 4): "Nb",
                  (4, 5): "Mo", (4, 6): "Tc", (4, 7): "Ru", (4, 8): "Rh",
                  (4, 9): "Pd", (4,10): "Ag", (4,11): "Cd",
                  (4,12): "In", (4,13): "Sn", (4,14): "Sb", (4,15): "Te",
                  (4,16): "I",  (4,17): "Xe",

    (5, 0): "Cs", (5, 1): "Ba", (5, 2): "Ln",  (5, 3): "Hf", (5, 4): "Ta",
                  (5, 5): "W",  (5, 6): "Re",  (5, 7): "Os", (5, 8): "Ir",
                  (5, 9): "Pt", (5,10): "Au", (5,11): "Hg",
                  (5,12): "Tl", (5,13): "Pb", (5,14): "Bi", (5,15): "Po",
                  (5,16): "At", (5,17): "Rn",

    (6, 0): "Fr", (6, 1): "Ra", (6, 2): "An",
}

MAX_ROW = max(r for (r, c) in TABLE_POSITIONS.keys())
MAX_COL = max(c for (r, c) in TABLE_POSITIONS.keys())

###############################################################################
# CELL DIMENSIONS
###############################################################################
CELL_INNER_HEIGHT = 2
CELL_INNER_WIDTH  = 3
CELL_TOTAL_HEIGHT = CELL_INNER_HEIGHT + 2
CELL_TOTAL_WIDTH  = CELL_INNER_WIDTH + 2

###############################################################################
# CLASSIFICATION COLORS
###############################################################################
CLASS_TO_COLOR = {
    "alkali metal":         2,
    "alkaline earth metal": 3,
    "transition metal":     4,
    "post-transition metal":5,
    "metalloid":            6,
    "nonmetal":             7,
    "halogen":              8,
    "noble gas":            9
}
PLACEHOLDER_PAIR = 10
HIGHLIGHT_PAIR   = 11

###############################################################################
# INFO BOX
###############################################################################
INFO_BOX_TOP    = 1
INFO_BOX_LEFT   = 20
INFO_BOX_HEIGHT = 10
INFO_BOX_WIDTH  = 30

def draw_cell_with_border(stdscr, top_y, left_x, highlight=False):
    """Draw one periodic-table cell (including the border)."""
    import curses
    
    if highlight:
        stdscr.attron(curses.color_pair(HIGHLIGHT_PAIR) | curses.A_BOLD | curses.A_REVERSE)
    else:
        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)

    ul = BOX_CHARS["ul"]
    ur = BOX_CHARS["ur"]
    ll = BOX_CHARS["ll"]
    lr = BOX_CHARS["lr"]
    h  = BOX_CHARS["h"]
    v  = BOX_CHARS["v"]

    # Top border
    stdscr.addch(top_y, left_x, ul)
    for i in range(CELL_TOTAL_WIDTH - 2):
        stdscr.addch(top_y, left_x + 1 + i, h)
    stdscr.addch(top_y, left_x + CELL_TOTAL_WIDTH - 1, ur)

    # Middle lines
    for line_idx in range(CELL_INNER_HEIGHT):
        row_y = top_y + 1 + line_idx
        stdscr.addch(row_y, left_x, v)
        stdscr.addch(row_y, left_x + CELL_TOTAL_WIDTH - 1, v)

    # Bottom border
    bottom_y = top_y + CELL_TOTAL_HEIGHT - 1
    stdscr.addch(bottom_y, left_x, ll)
    for i in range(CELL_TOTAL_WIDTH - 2):
        stdscr.addch(bottom_y, left_x + 1 + i, h)
    stdscr.addch(bottom_y, left_x + CELL_TOTAL_WIDTH - 1, lr)

    if highlight:
        stdscr.attroff(curses.color_pair(HIGHLIGHT_PAIR) | curses.A_BOLD | curses.A_REVERSE)
    else:
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

def draw_info_box(stdscr, top_y, left_x, lines):
    """Draw the info box with bold box-drawing and center each text line."""
    import curses
    
    stdscr.attron(curses.color_pair(1) | curses.A_BOLD)

    ul = BOX_CHARS["ul"]
    ur = BOX_CHARS["ur"]
    ll = BOX_CHARS["ll"]
    lr = BOX_CHARS["lr"]
    h  = BOX_CHARS["h"]
    v  = BOX_CHARS["v"]

    # Top border
    stdscr.addch(top_y, left_x, ul)
    for i in range(INFO_BOX_WIDTH - 2):
        stdscr.addch(top_y, left_x + 1 + i, h)
    stdscr.addch(top_y, left_x + INFO_BOX_WIDTH - 1, ur)

    # Sides
    for row_i in range(1, INFO_BOX_HEIGHT - 1):
        stdscr.addch(top_y + row_i, left_x, v)
        stdscr.addch(top_y + row_i, left_x + INFO_BOX_WIDTH - 1, v)

    # Bottom
    bottom_y = top_y + INFO_BOX_HEIGHT - 1
    stdscr.addch(bottom_y, left_x, ll)
    for i in range(INFO_BOX_WIDTH - 2):
        stdscr.addch(bottom_y, left_x + 1 + i, h)
    stdscr.addch(bottom_y, left_x + INFO_BOX_WIDTH - 1, lr)

    stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

    content_width = INFO_BOX_WIDTH - 2
    content_height = INFO_BOX_HEIGHT - 2

    for i, (text, color_idx) in enumerate(lines[:content_height]):
        line_str = text.center(content_width)
        if color_idx:
            stdscr.attron(curses.color_pair(color_idx) | curses.A_BOLD)
            stdscr.addstr(top_y + 1 + i, left_x + 1, line_str)
            stdscr.attroff(curses.color_pair(color_idx) | curses.A_BOLD)
        else:
            stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
            stdscr.addstr(top_y + 1 + i, left_x + 1, line_str)
            stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

def handle_move(current_r, current_c, direction):
    """
    Move through TABLE_POSITIONS skipping empty spaces.
    direction is one of: 'left', 'right', 'up', 'down'.
    We'll find the next valid (r, c) with an existing element.
    If none is found, we return the same (r, c).
    """
    if direction == 'left':
        # find the largest col < current_c for which (current_r, col) in TABLE_POSITIONS
        for col in range(current_c - 1, -1, -1):
            if (current_r, col) in TABLE_POSITIONS:
                return (current_r, col)
        return (current_r, current_c)

    elif direction == 'right':
        # find the smallest col > current_c for which (current_r, col) in TABLE_POSITIONS
        for col in range(current_c + 1, MAX_COL+1):
            if (current_r, col) in TABLE_POSITIONS:
                return (current_r, col)
        return (current_r, current_c)

    elif direction == 'up':
        # find the largest row < current_r for which (row, current_c) in TABLE_POSITIONS
        for row in range(current_r - 1, -1, -1):
            if (row, current_c) in TABLE_POSITIONS:
                return (row, current_c)
        return (current_r, current_c)

    elif direction == 'down':
        # find the smallest row > current_r for which (row, current_c) in TABLE_POSITIONS
        for row in range(current_r + 1, MAX_ROW+1):
            if (row, current_c) in TABLE_POSITIONS:
                return (row, current_c)
        return (current_r, current_c)

    else:
        return (current_r, current_c)

def main(stdscr):
    import curses
    
    curses.curs_set(0)
    curses.start_color()

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)   # default
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)    # alkali metal
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)   # alkaline earth
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # transition
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # post-transition
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)    # metalloid
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)   # nonmetal
    curses.init_pair(8, curses.COLOR_RED, curses.COLOR_BLACK)     # halogen
    curses.init_pair(9, curses.COLOR_BLUE, curses.COLOR_BLACK)    # noble gas
    curses.init_pair(10, curses.COLOR_CYAN, curses.COLOR_BLACK)   # placeholders
    curses.init_pair(11, curses.COLOR_WHITE, curses.COLOR_BLACK)  # highlight

    # Minimal terminal check
    needed_rows = max((MAX_ROW+1)*CELL_TOTAL_HEIGHT, INFO_BOX_TOP + INFO_BOX_HEIGHT + 2)
    needed_cols = max((MAX_COL+1)*CELL_TOTAL_WIDTH, INFO_BOX_LEFT + INFO_BOX_WIDTH + 2)
    rows, cols = stdscr.getmaxyx()
    if rows < needed_rows or cols < needed_cols:
        curses.endwin()
        print(f"Terminal too small: {rows}x{cols}, need {needed_rows}x{needed_cols} minimum.")
        sys.exit(1)

    # Start at H
    current_row, current_col = 0, 0

    while True:
        stdscr.clear()

        # Draw the table cells
        for (r, c), symbol in TABLE_POSITIONS.items():
            top_y = r * CELL_TOTAL_HEIGHT
            left_x = c * CELL_TOTAL_WIDTH
            highlight = (r == current_row and c == current_col)
            draw_cell_with_border(stdscr, top_y, left_x, highlight)

        # Print the atomic number + symbol
        for (r, c), symbol in TABLE_POSITIONS.items():
            y = r * CELL_TOTAL_HEIGHT
            x = c * CELL_TOTAL_WIDTH
            interior_y1 = y + 1
            interior_y2 = y + 2
            interior_x = x + 1

            is_selected = (r == current_row and c == current_col)

            z_str = "   "
            if symbol not in ("Ln", "An"):
                try:
                    z = Elements.atomic_number(symbol)
                    z_str = f"{z:>3}"
                except KeyError:
                    z_str = "?? "

            if is_selected:
                stdscr.attron(curses.color_pair(HIGHLIGHT_PAIR) | curses.A_BOLD | curses.A_REVERSE)
            else:
                stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
            stdscr.addstr(interior_y1, interior_x, z_str)
            if is_selected:
                stdscr.attroff(curses.color_pair(HIGHLIGHT_PAIR) | curses.A_BOLD | curses.A_REVERSE)
            else:
                stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

            # Symbol in classification color
            if symbol in ("Ln", "An"):
                color_pair = PLACEHOLDER_PAIR
            else:
                try:
                    classif = Elements.classification(symbol)
                    color_pair = CLASS_TO_COLOR.get(classif, 1)
                except KeyError:
                    color_pair = 1

            attrs = curses.color_pair(color_pair) | curses.A_BOLD
            if is_selected:
                attrs |= curses.A_REVERSE

            sym_str = symbol.center(3)
            stdscr.attron(attrs)
            stdscr.addstr(interior_y2, interior_x, sym_str)
            stdscr.attroff(attrs)

        # Build info lines
        highlight_symbol = TABLE_POSITIONS.get((current_row, current_col))
        lines_for_box = []
        if highlight_symbol in ("Ln", "An"):
            # placeholders
            lines_for_box = [
                ("", None),
                ("", None),
                ("", None),
                ("Lanthanides" if highlight_symbol=="Ln" else "Actinides", None),
                ("not individually shown.", None),
                ("", None), ("", None), ("", None), ("", None),
            ]
        else:
            z = p = g = None
            mass = en = None
            vdw = cov = None
            name = classification = None

            try: z = Elements.atomic_number(highlight_symbol)
            except: pass
            try: p = Elements.period(highlight_symbol)
            except: pass
            try: g = Elements.group(highlight_symbol)
            except: pass
            try: mass = Elements.mass(highlight_symbol, "u")
            except: pass
            try: en = Elements.electronegativity(highlight_symbol, "pauling")
            except: pass
            try: vdw = Elements.vdw_radius(highlight_symbol, "Å")
            except: pass
            try:
                cov = Elements.covalent_radius(highlight_symbol, "single","cordero","Å")
            except:
                pass
            try: name = Elements.name(highlight_symbol)
            except: pass
            try: classification = Elements.classification(highlight_symbol)
            except: pass

            if classification and classification in CLASS_TO_COLOR:
                line_color = CLASS_TO_COLOR[classification]
            else:
                line_color = 1

            ln1 = f"{z}" if z else ""
            if p and g:
                ln2 = f"Period {p} Group {g}"
            else:
                ln2 = ""
            ln3 = highlight_symbol if highlight_symbol else ""
            ln4 = name if name else ""
            ln5 = f"{mass:.3f} amu" if mass else ""
            ln6 = classification if classification else ""
            if cov and vdw:
                ln7 = f"Coval: {cov:.2f} Å vdW: {vdw:.2f} Å"
            else:
                ln7 = ""
            ln8 = f"Electroneg: {en:.2f}" if en else ""

            lines_for_box = [
                (ln1, None),
                (ln2, None),
                (ln3, line_color),
                (ln4, line_color),
                (ln5, None),
                (ln6, None),
                (ln7, None),
                (ln8, None),
                ("", None),
            ]

        draw_info_box(stdscr, INFO_BOX_TOP, INFO_BOX_LEFT, lines_for_box)

        # instructions
        help_y = (MAX_ROW+1)*CELL_TOTAL_HEIGHT + 1
        stdscr.addstr(help_y, 0, "[Arrow keys or hjkl: move]  [q: quit]")

        stdscr.refresh()

        ch = stdscr.getch()

        # vi-style keys
        if ch == ord('h'):
            new_r, new_c = handle_move(current_row, current_col, 'left')
            current_row, current_col = new_r, new_c
        elif ch == ord('l'):
            new_r, new_c = handle_move(current_row, current_col, 'right')
            current_row, current_col = new_r, new_c
        elif ch == ord('k'):
            new_r, new_c = handle_move(current_row, current_col, 'up')
            current_row, current_col = new_r, new_c
        elif ch == ord('j'):
            new_r, new_c = handle_move(current_row, current_col, 'down')
            current_row, current_col = new_r, new_c

        elif ch == curses.KEY_LEFT:
            new_r, new_c = handle_move(current_row, current_col, 'left')
            current_row, current_col = new_r, new_c
        elif ch == curses.KEY_RIGHT:
            new_r, new_c = handle_move(current_row, current_col, 'right')
            current_row, current_col = new_r, new_c
        elif ch == curses.KEY_UP:
            new_r, new_c = handle_move(current_row, current_col, 'up')
            current_row, current_col = new_r, new_c
        elif ch == curses.KEY_DOWN:
            new_r, new_c = handle_move(current_row, current_col, 'down')
            current_row, current_col = new_r, new_c

        elif ch == ord('q'):
            break

    curses.endwin()

if __name__ == "__main__":
    curses.wrapper(main)
