#!/usr/bin/env pyton

from . import wgcheckbox
import weakref

class FormControlCheckbox(wgcheckbox.Checkbox):
    def __init__(self, *args, **keywords):
        super(FormControlCheckbox, self).__init__(*args, **keywords)
        self._visibleWhenSelected    = []
        self._notVisibleWhenSelected = []

    def addVisibleWhenSelected(self, w):
        """Add a widget to be visible only when this box is selected"""
        self._register(w, vws=True)
    
    def addInvisibleWhenSelected(self, w):
        self._register(w, vws=False)
        
    def _register(self, w, vws=True):
        if vws:
            working_list = self._visibleWhenSelected
        else:
            working_list = self._notVisibleWhenSelected
            
        if w in working_list:
            pass
        else:
            try:
                working_list.append(weakref.proxy(w))
            except TypeError:
                working_list.append(w)
        
        self.updateDependents()
    
    def updateDependents(self):
        # Support dependents with multiple FormControlCheckbox parents
        # A dependent should be visible only when all parents agree
        if self.value:
            for w in self._visibleWhenSelected:
                try:
                    w.fc_visible
                except AttributeError:
                    w.fc_visible = {}
                w.fc_visible[self.name] = True
            for w in self._notVisibleWhenSelected:
                try:
                    w.fc_visible
                except AttributeError:
                    w.fc_visible = {}
                w.fc_visible[self.name] = False
        else:
            for w in self._visibleWhenSelected:
                try:
                    w.fc_visible
                except AttributeError:
                    w.fc_visible = {}
                w.fc_visible[self.name] = False
            for w in self._notVisibleWhenSelected:
                try:
                    w.fc_visible
                except AttributeError:
                    w.fc_visible = {}
                w.fc_visible[self.name] = True
        for w in self._visibleWhenSelected + self._notVisibleWhenSelected:
            w.hidden = False in w.fc_visible.values()
            w.editable = not False in w.fc_visible.values()
        self.parent.display()

    def h_toggle(self, *args):
        super(FormControlCheckbox, self).h_toggle(*args)
        self.updateDependents()
        
    def set_value(self, value):
        self.value = value
        self.display()

    def display(self):
        self.updateDependents()
        super()
