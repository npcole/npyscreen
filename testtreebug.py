import npyscreen

tree_data = npyscreen.NPSTreeData()
tree_data.newChild(content={'a': 1})
q = tree_data.newChild(content={'b': 2})
q.newChild(content={'c': 4})

class MyTreeLineAnnotated(npyscreen.TreeLineAnnotated):
    def getAnnotationAndColor(self):
        # AHH, self.value is an empty str, this fails.
        #if self.value:
        content = str(self.value)
        return (content, self._annotatecolor)
    
    def display_value(self, vl):
        return str(vl)

class MyTree(npyscreen.MultiLineTreeNew):
    _contained_widgets = MyTreeLineAnnotated
    def display_value(self, vl):
        return vl

class MyForm(npyscreen.Form):
    def create(self):
        self.series_view = self.add(MyTree, values=tree_data)

def myFunction(*args):
    F = MyForm(name = "My Form")
    F.edit()

npyscreen.wrapper_basic(myFunction)
