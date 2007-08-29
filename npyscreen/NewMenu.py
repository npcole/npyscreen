#!/usr/bin/env python
# encoding: utf-8
import weakref


class NewMenu(object):
    """docstring for NewMenu"""
    def __init__(self, name=None):
        self.name      = name
        self._menuList = []
        
    def addItem(self, *args, **keywords):
        _itm = MenuItem(*args, **keywords)
        self._menuList.append(_itm)
    
    def addSubmenu(self, submenu):
        "Not recommended. Use addNewSubmenu instead"
        _itm = submenu
        self._menuList.append(submenu)
    
    def addNewSubmenu(self, *args, **keywords):
        _mnu = NewMenu(*args, **keywords)
        self._menuList.append(_mnu)
        return weakref.proxy(_mnu)
    
    def getItemObjects(self):
        return self._menuList
        

class MenuItem(object):
    """docstring for MenuItem"""
    def __init__(self, text='', onSelect=None):
        self.setText(text)
        self.setOnSelect(onSelect)
        
    def setText(self, text):
        self._text = text
        
    def getText(self):
        return self._text
    
    def setOnSelect(self, onSelect):
        self.onSelectFunction = onSelect
        
    def do(self):
        return self.onSelectFunction()
    
    
        


def main():
    print "When I left you I was but the learner."


if __name__ == '__main__':
    main()

