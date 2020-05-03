from . import fmPopup
from . import wgmultiline
from . import fmPopup
import curses
import textwrap
import threading

class ConfirmCancelPopup(fmPopup.ActionPopup):
    def on_ok(self):
        self.value = True
    def on_cancel(self):
        self.value = False

class YesNoPopup(ConfirmCancelPopup):
    OK_BUTTON_TEXT = "Yes"
    CANCEL_BUTTON_TEXT = "No"
    
def _prepare_message(message):
    if isinstance(message, list) or isinstance(message, tuple):
        return "\n".join([ s.rstrip() for s in message])
        #return "\n".join(message)
    else:
        return message

def _wrap_message_lines(message, line_length):
    lines = []
    for line in message.split('\n'):
        lines.extend(textwrap.wrap(line.rstrip(), line_length))
    return lines
    
def notify(message, title="Message", form_color='STANDOUT', 
            wrap=True, wide=False,
            ):
    message = _prepare_message(message)
    if wide:
        F = fmPopup.PopupWide(name=title, color=form_color)
    else:
        F   = fmPopup.Popup(name=title, color=form_color)
    F.preserve_selected_widget = True
    mlw = F.add(wgmultiline.Pager,)
    mlw_width = mlw.width-1
    if wrap:
        message = _wrap_message_lines(message, mlw_width)
    mlw.values = message
    F.display()
    
def notify_confirm(message, title="Message", form_color='STANDOUT', wrap=True, wide=False,
                    editw = 0,):
    message = _prepare_message(message)
    if wide:
        F = fmPopup.PopupWide(name=title, color=form_color)
    else:
        F   = fmPopup.Popup(name=title, color=form_color)
    F.preserve_selected_widget = True
    mlw = F.add(wgmultiline.Pager,)
    mlw_width = mlw.width-1
    if wrap:
        message = _wrap_message_lines(message, mlw_width)
    else:
        message = message.split("\n")
    mlw.values = message
    F.editw = editw
    F.edit()

def notify_wait(*args, **keywords):
    notify(*args, **keywords)
    curses.napms(3000)
    curses.flushinp()    
    
    
def notify_ok_cancel(message, title="Message", form_color='STANDOUT', wrap=True, editw = 0,):
    message = _prepare_message(message)
    F   = ConfirmCancelPopup(name=title, color=form_color)
    F.preserve_selected_widget = True
    mlw = F.add(wgmultiline.Pager,)
    mlw_width = mlw.width-1
    if wrap:
        message = _wrap_message_lines(message, mlw_width)
    mlw.values = message
    F.editw = editw
    F.edit()
    return F.value

def notify_yes_no(message, title="Message", form_color='STANDOUT', wrap=True, editw = 0,):
    message = _prepare_message(message)
    F   = YesNoPopup(name=title, color=form_color)
    F.preserve_selected_widget = True
    mlw = F.add(wgmultiline.Pager,)
    mlw_width = mlw.width-1
    if wrap:
        message = _wrap_message_lines(message, mlw_width)
    mlw.values = message
    F.editw = editw
    F.edit()
    return F.value

def single_line_input(default_value="Input Text", title="Message", form_color='STANDOUT'):
    ''' Convenience function for requesting a single line of user input

    Args:
        default_value (str): The default value for the input textfield
        title (str): Title for the popup
        form_color (str): Color scheme used (as defined by the theme used)

    Returns:
        str: - None if the user pressed "Cancel"
             - Value of the text input field if the user pressed "OK"
    '''

    F = ConfirmCancelPopup(name=title, color=form_color)
    F.preserve_selected_widget = True
    tf = F.add(npyscreen.Textfield)
    tf.width = tf.width - 1
    tf.value = default_value
    F.edit()
    if F.value is True:
        return tf.value
    else:
        return None

def notify_loading(routine, frames = None, title = "Loading", delay = 150, form_color='STANDOUT'):
    ''' Convenience function for displaying an animation while a task is in progress.

    Args:
        routine (func): The function we are waiting for.
        frames ([str]): A list of string that are our animation's frames.
        title (str): Title for the popup.
        delay (int): The time between each frame.
        form_color (str): Color scheme used (as defined by the theme used).

    Returns:
        any: - Value returned by routine.
    '''

    global waiting
    global result

    waiting = True

    if frames == None:
        frames = [
            "   |/\n"
            "   +\n",

            "  \|  \n"
            "   +\n",

            "  \\ \n"
            " --+ \n",

            "    \n"
            " --+ \n"
            "  /",

            " \n"
            "   + \n"
            "  /|",

            "  \n"
            "   + \n"
            "   |\\",

            "  \n"
            "   +--\n"
            "    \\",

            "    /\n"
            "   +-- \n"
        ]

    def display_frame(frame, title,
            wrap=True, wide=False,
            ):
        F = fmPopup.LoadingPopup(name=title, color=form_color)
        F.preserve_selected_widget = True
        mlw = F.add(wgmultiline.Pager,)
        mlw.values = frame.split('\n')
        F.display()

    def capsule():
        ''' This function is intended to be ran inside a new thread.
            I use global for avoiding shadowing waiting and result variables.
        '''
        global waiting
        global result
        result = routine()
        waiting = False

    thread = threading.Thread(target=capsule)
    thread.start()
    i = 0
    while waiting:
        display_frame(frames[i], title)
        i = i + 1
        if(i >= len(frames)):
            i = 0
        curses.napms(150)
        curses.flushinp()
    thread.join()
    return result