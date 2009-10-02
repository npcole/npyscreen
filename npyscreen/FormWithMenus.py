#!/usr/bin/env python
# encoding: utf-8

import Form
import ActionForm
import NMenuDisplay

class FormBaseNewWithMenus(Form.FormBaseNew, NMenuDisplay.HasMenus):
    """The FormBaseNew class, but with a handling system for menus as well.  See the HasMenus class for details."""
    def __init__(self, *args, **keywords):
        super(FormBaseNewWithMenus, self).__init__(*args, **keywords)
        self.initialize_menus()
    
    def display_menu_advert_at(self):
        return self.lines-1, 1
    
    def draw_form(self):
        super(FormBaseNewWithMenus, self).draw_form()
        menu_advert = " " + self.__class__.MENU_KEY + ": Menu "
        y, x = self.display_menu_advert_at()
        self.curses_pad.addnstr(y, x, menu_advert, self.columns - x - 1)
    

class FormWithMenus(Form.Form, NMenuDisplay.HasMenus):
    """The Form class, but with a handling system for menus as well.  See the HasMenus class for details."""
    def __init__(self, *args, **keywords):
        super(FormWithMenus, self).__init__(*args, **keywords)
        self.initialize_menus()
    
    def display_menu_advert_at(self):
        return self.lines-1, 1
    
    def draw_form(self):
        super(FormWithMenus, self).draw_form()
        menu_advert = " " + self.__class__.MENU_KEY + ": Menu "
        y, x = self.display_menu_advert_at()
        self.curses_pad.addnstr(y, x, menu_advert, self.columns - x - 1)

# The following class does not inherit from FormWithMenus and so some code is duplicated.  
# The pig is getting to inherit edit() from ActionForm, but draw_form from FormWithMenus
class ActionFormWithMenus(ActionForm.ActionForm, NMenuDisplay.HasMenus):
    def __init__(self, *args, **keywords):
        super(ActionFormWithMenus, self).__init__(*args, **keywords)
        self.initialize_menus()
    def display_menu_advert_at(self):
        return self.lines-1, 1

    def draw_form(self):
        super(ActionFormWithMenus, self).draw_form()
        menu_advert = " " + self.__class__.MENU_KEY + ": Menu "
        y, x = self.display_menu_advert_at()
        self.curses_pad.addnstr(y, x, menu_advert, self.columns - x - 1)
        
class SplitFormWithMenus(FormWithMenus):
    """Just the same as the Title Form, but with a horizontal line"""
    def draw_form(self):
        MAXY, MAXX = self.curses_pad.getmaxyx()
        super(SplitFormWithMenus, self).draw_form()
        self.curses_pad.hline(MAXY//2-1, 1, curses.ACS_HLINE, MAXX-2)

    def get_half_way(self):
        return self.curses_pad.getmaxyx()[0] // 2



def main(arg):
    F = FormBaseNewWithMenus()

    def beep():
        curses.beep()
    def doNothing():
        pass

    q = None   
    
    M1 = F.new_menu(name='Menu1')
    M1.addItem('Beep', beep)
    M1.addItem('Nothing', doNothing)
    M1.addSubmenu(M1)

    F.add(titlefield.TitleText, name='Test')
    F.edit()
    print "I have you now"


if __name__ == '__main__':
    import curses
    import titlefield
    curses.wrapper(main)

