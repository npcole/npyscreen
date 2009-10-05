#!/usr/bin/env python
import weakref

class NPSTreeData(object):
    def __init__(self, content=None, parent=None, selected=False, hilight=False, expanded=True):
        self.setParent(parent)
        self.setContent(content)
        self.selected = selected
        self.hilight  = hilight
        self.expanded = expanded
        self._children = []
    
    def getContent(self):
        return self.content
        
    def getContentForDisplay(self):
        return str(self.content)
    
    def setContent(self, content):
        self.content = content
    
    def isSelected(self):
        return self.selected
    
    def isHighlighted(self):
        return self.hilight
    
    def setParent(self, parent):
        if parent == None:
            self.parent = None
        else:
            self.parent = weakref.proxy(parent)
    
    def findDepth(self, d=0):
        if self.parent == None:
            return d
        else:
            return(self.parent.findDepth(d+1))
    
    def hasChildren(self):
        if len(self._children) > 0:
            return True
        else:
            return False
    
    def getChildren(self):
        return self._children
    
    def newChild(self, *args, **keywords):
        c = NPSTreeData(parent=self, *args, **keywords)
        self._children.append(c)
        return weakref.proxy(c)
    
    def walkTree(self, onlyExpanded=True, ignoreRoot=True):
        #Iterate over Tree
        if not ignoreRoot:
            yield self
        if (not onlyExpanded) or (self.expanded):
            for child in self.getChildren():
                for node in child.walkTree(onlyExpanded=onlyExpanded, ignoreRoot=False):
                    yield node
    
    def getTreeAsList(self, onlyExpanded=True):
        _a = []
        for node in self.walkTree(onlyExpanded=onlyExpanded):
            _a.append(weakref.proxy(node))
        return _a

