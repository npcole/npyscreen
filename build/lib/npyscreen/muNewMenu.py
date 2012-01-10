#!/usr/bin/env python
# encoding: utf-8
import weakref


class NewMenu(object):
    """docstring for NewMenu"""
    def __init__(self, name=None):
        self.name      = name
        self._menuList = []
        self.enabled   = True
    
    def addItemsFromList(self, item_list):
        for l in item_list:
            if isinstance(l, MenuItem):
                self.addNewSubmenu(l)
            else:
                self.addItem(*l)

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
        return [itm for itm in self._menuList if itm.enabled]
        

class MenuItem(object):
    """docstring for MenuItem"""
    def __init__(self, text='', onSelect=None, document=None,):
        self.setText(text)
        self.setOnSelect(onSelect)
        self.setDocumentation(document)
        self.enabled = True
        
    def setText(self, text):
        self._text = text
        
    def getText(self):
        return self._text
    
    def setOnSelect(self, onSelect):
        self.onSelectFunction = onSelect
        
    def setDocumentation(self, document):
        self._help = document
    
    def getDocumentation(self):
        return self._help
    
    def getHelp(self):
        return self._help
    
    def do(self):
        return self.onSelectFunction()
