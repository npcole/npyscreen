import curses

def test_screen(screen):
    screen.addch(5,5, curses.ACS_HLINE)
    screen.addch(5,6, curses.ACS_HLINE)
    screen.refresh()
    curses.napms(2000)

curses.wrapper(test_screen)
