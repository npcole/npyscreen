import curses, locale
locale.setlocale(locale.LC_ALL, '') #NB This line is very important.
s = curses.initscr()
p = curses.newpad(24,80)
p.addstr(u'\u00c5 U+00C5 LATIN CAPITAL LETTER A WITH RING ABOVE\n'.encode('utf-8') )
p.addstr(u'\u00f5 U+00F5 LATIN SMALL LETTER O WITH TILDE\n'.encode('utf-8'))
p.refresh(0,0,0,0,20,80)
p.getstr()
curses.endwin()
