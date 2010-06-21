from . import fmPopup
from . import wgmultiline
from . import fmPopup
import curses
import textwrap

class ConfirmCancelPopup(fmPopup.ActionPopup):
    def on_ok(self):
        self.value = True
    def on_cancel(self):
        self.value = False

class YesNoPopup(ConfirmCancelPopup):
    OK_BUTTTON_TEXT = "Yes"
    CANCEL_BUTTON_TEXT = "No"
    
def notify(message, title="Message", form_color='STANDOUT', wrap=True):
    F   = fmPopup.Popup(name=title, color=form_color)
    mlw = F.add(wgmultiline.Pager,)
    mlw_width = mlw.width-1
    if wrap:
        message = textwrap.wrap(message, mlw_width)
    mlw.values = message
    F.display()
    
def notify_confirm(message, title="Message", form_color='STANDOUT', wrap=True):
    F   = fmPopup.Popup(name=title, color=form_color)
    mlw = F.add(wgmultiline.Pager,)
    mlw_width = mlw.width-1
    if wrap:
        message = textwrap.wrap(message, mlw_width)
    mlw.values = message
    F.edit()

def notify_wait(*args, **keywords):
    notify(*args, **keywords)
    curses.napms(3000)
    curses.flushinp()    
    
    
def notify_ok_cancel(message, title="Message", form_color='STANDOUT', wrap=True):
    F   = ConfirmCancelPopup(name=title, color=form_color)
    mlw = F.add(wgmultiline.Pager,)
    mlw_width = mlw.width-1
    if wrap:
        message = textwrap.wrap(message, mlw_width)
    mlw.values = message
    F.edit()
    return F.value

def notify_yes_no(message, title="Message", form_color='STANDOUT', wrap=True):
    F   = YesNoPopup(name=title, color=form_color)
    mlw = F.add(wgmultiline.Pager,)
    mlw_width = mlw.width-1
    if wrap:
        message = textwrap.wrap(message, mlw_width)
    mlw.values = message
    F.edit()
    return F.value

    