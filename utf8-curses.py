import curses, locale
locale.setlocale(locale.LC_ALL, '')
s = curses.initscr()
s.addstr(u'\u00c5 U+00C5 LATIN CAPITAL LETTER A WITH RING ABOVE\n'.encode('utf-8') )
s.addstr(u'\u00f5 U+00F5 LATIN SMALL LETTER O WITH TILDE\n'.encode('utf-8'))
s.refresh()
s.getstr()
curses.endwin()
