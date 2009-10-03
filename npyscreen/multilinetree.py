#!/usr/bin/python
import multiline
import checkbox
import selectone
import NPSTree
import weakref

class MultiLineTree(multiline.MultiLine):
    def _setMyValues(self, tree):
        if not isinstance(tree, NPSTree.NPSTreeData):
            raise TypeError, "MultiLineTree widget can only contain a NPSTreeData object in its values attribute"
        else:
            self._myFullValues = tree
    
    def _getApparentValues(self):
        return self._myFullValues.getTreeAsList()
    
    def _walkMyValues(self):
        return self._myFullValues.walkTree()
    
    def _delMyValues(self):
        self._myFullValues = None
    
    values = property(_getApparentValues, _setMyValues, _delMyValues)
    
    def get_tree_display(self, vl):
        dp = vl.findDepth()
        dp -= 1
        if dp > 0:
            control_chars = "| " * (dp) + "|-"
        else:
            control_chars = "| " * (dp) + "|-"
        if vl.hasChildren():
            if vl.expanded:
                control_chars = control_chars + "+"
            else:   
                control_chars = control_chars + ">"
        else:
            control_chars = control_chars + ""
        return control_chars
    
    def display_value(self, vl):
        return self.get_tree_display(vl) + "  " + str(vl.getContentForDisplay()) + "  "
    
class SelectOneTree(MultiLineTree):
    _contained_widgets = checkbox.RoundCheckBox
    def _print_line(self, line, value_indexer):
        try:
            line.value = self.values[value_indexer]
            line.hide = False
            if (self.values[value_indexer] in self.value and (self.value is not None)):
                line.show_bold = True
                line.name = self.display_value(self.values[value_indexer])
                line.value = True
            else:
                line.show_bold = False
                line.name = self.display_value(self.values[value_indexer])
                line.value = False
            if value_indexer in self._filtered_values_cache:
                line.important = True
            else:
                line.important = False
        except IndexError:
            line.name = None
            line.hide = True

        line.highlight= False
    
    def update(self, clear=True):
        if self.hidden:
            self.clear()
            return False
        # Make sure that self.value is a list
        if not hasattr(self.value, "append"):
            if self.value is not None:
                self.value = [self.value, ]
            else:
                self.value = []

        super(SelectOneTree, self).update(clear=clear)

    def h_select(self, ch):
        try:
            self.value = [weakref.proxy(self.values[self.cursor_line]),]
        except TypeError:
            # Actually, this is inefficient, since with the NPSTree class (default) we will always be here - since by default we will 
            # try to create a weakref to a weakref, and that will fail with a type-error.  BUT we are only doing it on a keypress, so
            # it shouldn't create a huge performance hit, and is future-proof. Code replicated in h_select_exit
            self.value = [self.values[self.cursor_line],]
    
    def h_select_exit(self, ch):
        try:
            self.value = [weakref.proxy(self.values[self.cursor_line]),]
        except TypeError:
            # Actually, this is inefficient, since with the NPSTree class (default) we will always be here - since by default we will 
            # try to create a weakref to a weakref, and that will fail with a type-error.  BUT we are only doing it on a keypress, so
            # it shouldn't create a huge performance hit, and is future-proof.
            self.value = [self.values[self.cursor_line],]
        if self.return_exit:
            self.editing = False
            self.how_exited=True
            
    def h_set_filtered_to_selected(self, ch):
        if len(self._filtered_values_cache) < 2:
            self.value = self.get_filtered_values()
        else:
            # There is an error - trying to select too many things.
            curses.beep()

        




if __name__ == '__main__':
    
    def testme(sa):
        import screen_area
        import Form
        #SA = screen_area.ScreenArea()
        
        Tree = NPSTree.NPSTreeData(content = "Test",)
        n1   = Tree.newChild(content = "TestChild")
        gc1  = n1.newChild(content = "GrandChild1")
        gc2  = n1.newChild(content = "GrandChild2")
        gc3  = n1.newChild(content = "GrandChild3")
        ggc1 = gc1.newChild(content = "Great Grand Child1")
        ggc2 = gc1.newChild(content = "Great Grand Child2")
        ggc3 = gc1.newChild(content = "Great Grand Child3")
        n2   = Tree.newChild(content = "newChild2")
        
        
        
        SA = Form.Form()
        w = SelectOneTree(SA, 
            #relx=5, 
            #rely=2, 
            values=Tree, 
            #max_height=5, 
            slow_scroll=True, scroll_exit=False)
        SA.display()
        w.edit()
    
    import curses.wrapper
    print curses.wrapper(testme)
    print "No, I'll never join you"
