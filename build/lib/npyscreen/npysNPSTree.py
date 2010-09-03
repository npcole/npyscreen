#!/usr/bin/env python
import weakref
import collections

class NPSTreeData(object):
    CHILDCLASS = None
    def __init__(self, content=None, parent=None, selected=False, hilight=False, expanded=True, ignoreRoot=True):
        self.setParent(parent)
        self.setContent(content)
        self.selected = selected
        self.hilight  = hilight
        self.expanded = expanded
        self._children = []
        self.ignoreRoot = ignoreRoot
    
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
            self._parent = None
        else:
            self._parent = weakref.proxy(parent)
    
    def getParent(self):
        return self._parent
    
    def findDepth(self, d=0):
        depth = d
        parent = self.getParent()
        while parent:
            d += 1
            parent = parent.getParent()
        if self.ignoreRoot == True:
            d -= 1
            if d < 0:
                raise ValueError
            else:
                return d
        else:
            return d
        # Recursive
        #if self._parent == None:
        #    return d
        #else:
        #    return(self._parent.findDepth(d+1))
    
    def hasChildren(self):
        if len(self._children) > 0:
            return True
        else:
            return False
    
    def getChildren(self):
        for c in self._children:
            try:
                yield weakref.proxy(c)
            except:
                yield c
                
    def getChildrenObjects(self):
        return self._children[:]
    
    def _getChildrenList(self):
        return self._children
    
    def newChild(self, *args, **keywords):
        if self.CHILDCLASS:
            cld = self.CHILDCLASS
        else:
            cld = type(self)
        c = cld(parent=self, *args, **keywords)
        self._children.append(c)
        return weakref.proxy(c)
        
    def removeChild(self, child):
        new_children = []
        for ch in self._children:
            # do it this way because of weakref equality bug.
            if not ch.getContent() == child.getContent():
                new_children.append(ch)
            else:
                ch.setParent(None)
        self._children = new_children
    
        

    def walkTree(self, onlyExpanded=True, ignoreRoot=True, sort=None, key=None):
        #Iterate over Tree
        if not ignoreRoot:
            yield self
        nodes_to_yield = collections.deque() # better memory management than a list for pop(0)
        if self.expanded:
            if sort:
                # This and the similar block below could be combined into a nested function
                if key:
                    nodes_to_yield.extend(sorted(self.getChildren(), key=key))
                else:
                    nodes_to_yield.extend(sorted(self.getChildren()))
            else:
                nodes_to_yield.extend(self.getChildren())
            while nodes_to_yield:
                child = nodes_to_yield.popleft()
                if child.expanded:
                    # This and the similar block above could be combined into a nested function
                    if sort:
                        if key:
                            nodes_to_yield.extendleft(sorted(child.getChildren(), key=key))
                        else:
                            nodes_to_yield.extendleft(sorted(child.getChildren()))
                    else:
                        #for node in child.getChildren():
                        #    if node not in nodes_to_yield:
                        #        nodes_to_yield.appendleft(node)
                        nodes_to_yield.extendleft(child.getChildren())
                yield child
    
    def _walkTreeRecursive(self,onlyExpanded=True, ignoreRoot=True,):
        #This is an old, recursive version
        if (not onlyExpanded) or (self.expanded):
            for child in self.getChildren():
                for node in child.walkTree(onlyExpanded=onlyExpanded, ignoreRoot=False):
                    yield node
        
    def getTreeAsList(self, onlyExpanded=True, sort=None, key=None):
        _a = []
        for node in self.walkTree(onlyExpanded=onlyExpanded, ignoreRoot=self.ignoreRoot, sort=sort, key=key):
            try:
                _a.append(weakref.proxy(node))
            except:
                _a.append(node)
        return _a

