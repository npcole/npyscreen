import npyscreen
import curses

def simpletest(screen):
	SA = npyscreen.Form()
	w = npyscreen.Textfield(SA, )
	w.value = u'\u00c5 U+00C5 LATIN CAPITAL LETTER A WITH RING ABOVE\n'.encode('utf-8') 
	w.edit()
	w.update()
	

if __name__ == "__main__":
	curses.wrapper(simpletest)

