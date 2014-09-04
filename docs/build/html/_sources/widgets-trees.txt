Widgets: Trees and Tree displays
********************************


Representing Tree Data
++++++++++++++++++++++

TreeData
    The TreeData class is used to represent tree objects.  Each node of the tree, including the root node, is an NPSTreeData instance.  Each node may have its own content, a parent or children.

    The content of each node is either set when it is created or using the *.set_content* method.

    *get_content()* returns the content.

    *get_content_for_display()* is used by the widgets that display trees, which expect it to return a string that can be displayed to the user to represent the content.  You might want to overload this method.

    *new_child(content=...)* creates a new child node.

    *selectable* If this attribute is true the user can mark a value as 'selected'. This is used by MLTreeMultiSelect widget, and is True by default.

    *ignore_root* This attribute controls whether the root node of the tree is displayed to the user.

    *expanded* This attribute controls whether this branch of the tree is expanded, assuming the node has any children.

    *sort* This attribute controls whether the tree should be sorted.

    *sort_function* If the tree is sorted, the function named in this attribute will be used as a key to sort the tree when it is being displayed.

    *walk_tree(only_expanded=True, ignore_root=True, sort=None, sort_function=None)*  Iterate over the tree.  You can override the standard sort and sort functions, and decide whether or not to iterate over only nodes of the tree that are marked as expanded.


Trees
+++++

MLTree, MLTreeAction
    The *values* attribute of this class must store an NPSTree instance.
    However, if you wish you can override the method *convertToTree* of this
    class.  This method should return an NPSTree instance.  The function will be
    called automatically whenever *values* is assigned.

    By default this class uses *TreeLine* widgets 
    to display each line of the tree.  In derived classes You can change this by changing
    the class attribute *_contained_widgets*.  The class attribute `_contained_widget_height` 
    specifies how many lines of the screen each widget should be given.

MLTreeAnnotated, MLTreeAnnotatedAction
    By default this class uses *TreeLineAnnotated* widgets to display each line of the tree.
    In derived classes You can change this by changing the class 
    attribute *_contained_widgets*.

MLTreeMultiSelect
    *New in version 2.0pre70*
    
    This class allows you to select multiple items of a tree.  You can select which nodes of NPSTreeData the user is able to select by setting the attribute *selectable* on that node.
    
    The method *get_selected_objects(self, return_node=True,)* returns an generator object that lists the nodes that are selected.  If return_node is True, the actual node itself is yielded, otherwise the value of *node.getContent()* is yielded instead.
    
    *New in Version 2.0pre71*   If the attribute *select_cascades* is True (which can be set by passing the argument *select_cascades* at the time of creation or setting the attribute directly later), selecting a node will automatically select any selectable nodes under the selected node. This is set to True by default.
    
    The selected nodes also have their attribute *selected* set to True, and so you can walk through the tree to find them if you prefer.
    
    The widget used to display each line is *TreeLineSelectable*.

MLTreeMultiSelectAnnotated
    *New in version 2.0pre71*
    
    A version of the MLTreeMultiSelect class that uses *TreeLineSelectableAnnotated* as its display widgets.



Deprecated Tree Classes
+++++++++++++++++++++++
NPSTreeData
    DEPRECATED in favour of the TreeData class.  The NPSTreeData class is used to represent tree objects.  Each node of the tree, including the root node, is an NPSTreeData instance.  Each node may have its own content, a parent or children.

    The content of each node is either set when it is created or using the *.setContent* method.

    *.getContent* returns the content.

    *.getContentForDisplay* is used by the widgets that display trees, which expect it to return a string that can be displayed to the user to represent the content.  You might want to overload this method.

    *newChild(content=...)* creates a new child node.

    *selectable* (new in version 2.0pre70) If this attribute is true the user can mark a value as 'selected'. This is used by MLTreeMultiSelect widget, and is True by default.



MultiLineTree, SelectOneTree, and MultiLineTree
    These widgets all work in a very similar way to the non-Tree versions,
    except that they expect to contain an NPSTree in their .values attribute.
    The other major difference is that their .value attribute does not contain
    the index of the selected value(s), but the selected value(s)
    itself/themselves.  However, these classes are DEPRECATED in favour of the
    much improved *MLTree* and *MLTreeAction* classes. 


MultiLineTreeNew, MultiLineTreeNewAction
    *These classes are provided solely for compatibility with old code. New classes should use the MLTree and related classes*

    The *values* attribute of this class must store an NPSTree instance.
    However, if you wish you can override the method *convertToTree* of this
    class.  This method should return an NPSTree instance.  The function will be
    called automatically whenever *values* is assigned.


    By default this class uses *TreeLineAnnotated* widgets 
    to display each line of the tree.  In derived classes You can change this by changing
    the class attribute *_contained_widgets*.
    
MutlilineTreeNewAnnotated, MultilineTreeNewAnnotatedAction
    *These classes are provided solely for compatibility with old code. New classes should use the MLTree and related classes*
    
    By default this class uses *TreeLineAnnotated* widgets 
    to display each line of the tree.  In derived classes You can change this by changing
    the class attribute *_contained_widgets*.
