import curses
import curses.textpad
import sys
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Any, Callable
from unittest import TestLoader, TextTestRunner

from tdd.expr import evaluate_infix, infix_to_postfix

Window = Any


@dataclass
class MenuOption:
    title: str
    action: Callable[[Window], None]


def run_basic_example_action(window):
    window.erase()
    window.box()

    window.addstr(2, 2, 'PLEASE INPUT AN INFIX EXPRESSION AND PRESS ENTER.')
    window.addstr(3, 2, 'ALLOWED OPERATORS: +, -, *, /, (, ).')
    window.addstr(4, 2, 'EXAMPLE: 1+2*3')
    window.move(0, 0)

    y, x = window.getyx()
    textbox_window = curses.newwin(curses.LINES - 12, curses.COLS - 6, y + 8, x + 4)

    textbox = curses.textpad.Textbox(textbox_window)
    window.refresh()
    textbox_window.refresh()

    textbox.edit(lambda x: 7 if x == 10 else x)
    infix = textbox.gather().replace(' ', '')

    textbox_window.erase()
    textbox_window.refresh()
    del textbox_window

    try:
        postfix = infix_to_postfix(infix)
    except Exception:
        window.addstr(6, 2, 'THERE WAS AN ERROR WHEN PARSING THE EXPRESSION.')
        window.addstr(7, 2, 'PLEASE MAKE SURE THE EXPRESSION IS SYNTACTICALLY CORRECT.')
    else:
        window.addstr(6, 2, f'INFIX: {infix}')
        window.addstr(7, 2, f'POSTFIX: {postfix}')
        window.addstr(9, 2, 'PRESS ANY KEY TO CONTINUE...')

    window.getch()


def run_complex_example_action(window):
    window.erase()
    window.box()

    window.addstr(2, 2, 'PLEASE INPUT AN INFIX EXPRESSION AND PRESS ENTER.')
    window.addstr(3, 2, 'ALLOWED OPERATORS: +, -, *, /, (, ).')
    window.addstr(4, 2, 'EXAMPLE: (1+2)*3+(4-5)/6')
    window.move(0, 0)

    y, x = window.getyx()
    textbox_window = curses.newwin(curses.LINES - 12, curses.COLS - 6, y + 8, x + 4)

    textbox = curses.textpad.Textbox(textbox_window)
    window.refresh()
    textbox_window.refresh()

    textbox.edit(lambda x: 7 if x == 10 else x)
    infix = textbox.gather().replace(' ', '')

    textbox_window.erase()
    textbox_window.refresh()
    del textbox_window

    try:
        result = evaluate_infix(infix)
    except Exception:
        window.addstr(6, 2, 'THERE WAS AN ERROR WHEN PARSING THE EXPRESSION.')
        window.addstr(7, 2, 'PLEASE MAKE SURE THE EXPRESSION IS SYNTACTICALLY CORRECT.')
    else:
        window.addstr(6, 2, f'INFIX: {infix}')
        window.addstr(7, 2, f'RESULT: {result}')
        window.addstr(9, 2, 'PRESS ANY KEY TO CONTINUE...')

    window.getch()


def run_tests_action(window):
    window.erase()
    window.box()

    y, x = window.getyx()
    output_window = curses.newwin(curses.LINES - 6, curses.COLS - 5, y + 3, x + 3)

    test_suite = TestLoader().discover(start_dir=Path(__file__).parent / 'tests')
    test_output = StringIO()
    TextTestRunner(test_output, verbosity=2).run(test_suite)

    output_window.addstr(0, 0, test_output.getvalue())
    output_window.addstr('\nPRESS ANY KEY TO CONTINUE...')
    window.refresh()
    output_window.refresh()
    window.getch()

    del output_window


def exit_action(window):
    sys.exit(0)


MENU_OPTIONS = [
    MenuOption(
        'BASIC EXAMPLE:\tCONVERT EXPRESSION FROM INFIX TO POSTFIX',
        run_basic_example_action,
    ),
    MenuOption(
        'COMPLEX EXAMPLE:\tCONVERT & EVALUATE INFIX EXPRESSION',
        run_complex_example_action,
    ),
    MenuOption('RUN TESTS', run_tests_action),
    MenuOption('EXIT', exit_action),
]

selected_option_index = 0


def draw_options(window):
    window.erase()
    window.box()
    for index, option in enumerate(MENU_OPTIONS):
        window.addstr(2 + index, 2, f'>> {option.title}')
        if selected_option_index == index:
            window.chgat(2 + index, 2, curses.COLS - 7, curses.A_REVERSE)


def main_loop(stdscr, menu_window):
    while True:
        draw_options(menu_window)
        stdscr.refresh()
        menu_window.refresh()

        global selected_option_index

        key = stdscr.getch()

        if key == ord('q'):
            return
        elif key == curses.KEY_DOWN:
            if selected_option_index + 1 < len(MENU_OPTIONS):
                selected_option_index += 1
        elif key == curses.KEY_UP:
            if selected_option_index > 0:
                selected_option_index -= 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            MENU_OPTIONS[selected_option_index].action(menu_window)


def main(stdscr):
    curses.curs_set(0)

    stdscr.addstr(0, 0, ' INFIX / POSTFIX EXPRESSION PARSER', curses.A_REVERSE)
    stdscr.chgat(-1, curses.A_REVERSE)

    stdscr.addstr(curses.LINES - 1, 0, ' KAMIL TUREK 2022', curses.A_REVERSE)
    stdscr.chgat(-1, curses.A_REVERSE)

    menu_window = curses.newwin(curses.LINES - 4, curses.COLS - 3, 2, 2)
    menu_window.box()
    menu_window.addstr(0, 2, 'CHOOSE AN OPTION')

    main_loop(stdscr, menu_window)


if __name__ == '__main__':
    curses.wrapper(main)
