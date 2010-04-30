from . import fmPopup
from . import wgmultiline
import curses
import textwrap

def notify(message, title="Message", form_color='STANDOUT'):
    F   = fmPopup.Popup(name=title, color=form_color)
    mlw = F.add(wgmultiline.Pager,)
    mlw_width = mlw.width-1
    message = textwrap.wrap(message, mlw_width)
    mlw.values = message
    F.display()
    
def notify_confirm(message, title="Message", form_color='STANDOUT'):
    F   = fmPopup.Popup(name=title, color=form_color)
    mlw = F.add(wgmultiline.Pager,)
    mlw_width = mlw.width-1
    message = textwrap.wrap(message, mlw_width)
    mlw.values = message
    F.edit()

def notify_wait(*args, **keywords):
    notify(*args, **keywords)
    curses.napms(3000)
    curses.flushinp()    