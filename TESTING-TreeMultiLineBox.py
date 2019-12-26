#!/usr/bin/env python
RETURN = []
import npyscreen

class SelectableTreeLine(npyscreen.TreeLineSelectableAnnotated):
    def calculate_area_needed(self):
        "Need two lines of screen, and any width going"
        return 2,0
    

class TestTree(npyscreen.MLTreeMultiSelect):
    _contained_widgets = SelectableTreeLine
    _contained_widget_height = 2


class TestApp(npyscreen.NPSApp):
    def main(self):
        F = npyscreen.Form(name = "Testing Tree class",)
        #wgtree = F.add(npyscreen.MLTree)
        wgtree = F.add(TestTree)
        
        treedata = npyscreen.NPSTreeData(content='Root', selectable=True,ignoreRoot=False)
        c1 = treedata.newChild(content='Child 1', selectable=True, selected=True)
        c2 = treedata.newChild(content='Child 2', selectable=True)
        g1 = c1.newChild(content='Grand-child 1', selectable=True)
        g2 = c1.newChild(content='Grand-child 2', selectable=True)
        g3 = c1.newChild(content='Grand-child 3')
        gg1 = g1.newChild(content='Great Grand-child 1', selectable=True)
        gg2 = g1.newChild(content='Great Grand-child 2', selectable=True)
        gg3 = g1.newChild(content='Great Grand-child 3')
        wgtree.values = treedata
        
        F.edit()
        
        global RETURN
        #RETURN = wgtree.values
        RETURN = wgtree.get_selected_objects()




if __name__ == "__main__":
    App = TestApp()
    App.run()   
    for v in RETURN:
        print(v)