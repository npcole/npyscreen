## ComboBox

def testme(sa):
    import screen_area
    A = screen_area.ScreenArea()
    #w = Checkbox(A, rely=10, relx=10, name='Check Box')
    #w.display()
    w2 = Checkbox(A, relx = 3, name='Check Box')
    w2.display()
    curses.napms(1500)

if __name__ == '__main__':
    import curses.wrapper
    curses.wrapper(testme)
    print("Use the force")


## DateCombo

def testing(src):
    import Form
    F = Form.Form()
    w = F.add(TitleDateCombo, name = "This is a Date")
    F.edit()
    return w.value



if __name__ == '__main__':
    import curses
    r = curses.wrapper(testing)
    print(r)
    print("Your faith in your friends is yours")

## EditMultiLine

def testme(sa):
    import screen_area
    import textbox
    SA = screen_area.ScreenArea()
    w = MultiLineEdit(SA, relx=5, rely=3, value=u"\u00c5 \u00c5 This\nis something of a test\nThis is line2 ", 
        max_height=5, max_width=70, slow_scroll=True, scroll_exit=False)

    w.value += "my height is %s" % w.height
    w.slow_scroll=False
    w.autowrap = True
    w.edit()
    w.display()

if __name__ == '__main__':
    import safewrapper
    safewrapper.wrapper(testme)
    print("Your powers are weak, old man")

## Form

def testmem(sa):
    import titlefield
    import textbox
    import slider
    import multiline
    while 1:
        F = Form(name="Testing")
        w = F.add_widget(titlefield.TitleText)
        str = "useable space = %s, %s; my height and width is: %s, %s" % (F.useable_space()[0], F.useable_space()[1], w.height, w.width)
        w.value = str
        w2 = F.add_widget(textbox.Textfield)
        str2 = "useable space = %s, %s; my height and width is: %s, %s" % (F.useable_space()[0], F.useable_space()[1], w2.height, w2.width)
        w2.value = str2
        w3 = F.add_widget(slider.Slider)
        #w4 = F.add_widget(multiline.MultiLine, height=5)
        F.display()

def testme(sa):
    import titlefield
    import textbox
    import slider
    import multiline

    F = TitleFooterForm(name="Testing")
    w = F.add_widget(titlefield.TitleText)
    str = "useable space = %s, %s; my height and width is: %s, %s" % (F.useable_space()[0], F.useable_space()[1], w.height, w.width)
    w.value = str
    w2 = F.add_widget(textbox.Textfield)
    str2 = "useable space = %s, %s; my height and width is: %s, %s" % (F.useable_space()[0], F.useable_space()[1], w2.height, w2.width)
    w2.value = str2
    w3 = F.add_widget(slider.Slider)
    #w4 = F.add_widget(multiline.MultiLine, height=5)
    F.display()
    F.edit()
    curses.napms(1500)
    

if __name__ == '__main__':
    curses.wrapper(testme)
    print("No Luke, I am your father")

## FormControlCheckBox

if __name__ == "__main__":
    def testform(*args):
        F = Form.Form()
        wtest = F.add(FormControlCheckbox, name="Test Me")
        w2    = F.add(checkbox.Checkbox, name="Just a Test")
        w3    = F.add(checkbox.Checkbox, name="Another Test")
        wtest.addVisibleWhenSelected(w2)
        wtest.addInvisibleWhenSelected(w3)
        F.edit()
    
    
    import Form
    import curses
    curses.wrapper(testform)
    
## FormMutt

def testme(w):
    import curses
    F = FormMutt()
    F.wStatus1.value = "Status Line "
    F.wStatus2.value = "Second Status Line "
    F.wMain.values   = [str(x) for x in range(500)]
    F.edit()

if __name__ == '__main__':
    import curses
    curses.wrapper(testme)
    print("No Luke, I am your father")

## FormWithMenus

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
    print("I have you now")


if __name__ == '__main__':
    import curses
    import titlefield
    curses.wrapper(main)

## Grid Tests

def testme(sa):
    import screen_area
    import Form
    SA = Form.Form()
    w = SA.add(SimpleGrid, column_width=4)
    vls = []
    start = 0
    for x in range(36):
        row = []
        for y in range(x, x+36):
            row.append(y)
        vls.append(row)
    w.values = vls
    w.value = (1,1)
    w.display()
    SA.edit()
        


if __name__ == '__main__':
    import curses.wrapper
    print(curses.wrapper(testme))
    print("No, I'll never join you")

## GridColTitles

def testme(sa):
    import screen_area
    import Form
    SA = Form.Form()
    w = SA.add(GridColTitles, column_width=6, col_titles=["One", "Two", "Three"])
    vls = []
    start = 0
    for x in range(36):
        row = []
        for y in range(x, x+36):
            row.append(y)
        vls.append(row)
    w.values = vls
    w.value = (1,1)
    w.display()
    SA.edit()



if __name__ == '__main__':
    import curses.wrapper
    print(curses.wrapper(testme))
    print("No, I'll never join you")

## Menu

def main(*args):
    mnu = Menu(name="Menu")
    mnu.add_item("Do Nothing", tstDoNothing)
    mnu.add_item("Do Nothing 2", tstDoNothing)
    mnu.add_item("Do Nothing 3", tstDoNothing)
    for x in range(10):
        mnu.add_item("Do Nothing x", tstDoNothing)
    mnu.edit()

def tstDoNothing():
    curses.beep()
    


if __name__ == '__main__':
    import curses.wrapper
    import curses
    curses.wrapper(main)

# MonthBox

def quicktest(scr):
    import screen_area
    SA = screen_area.ScreenArea()
    c = MonthBox(SA, allowTodaysDate=False, allowPastDate=True, rely=2, relx=6)
    c.value = datetime.date.today()
    c.edit()

if __name__ == "__main__":
    import curses
    import curses.wrapper
    curses.wrapper(quicktest)
    print("The circle is now complete")

## Multiline

def testme(sa):
    import screen_area
    import Form
    #SA = screen_area.ScreenArea()
    SA = Form.Form()
    w = MultiLine(SA, 
        #relx=5, 
        #rely=2,
        #width=5,
        values=['test1','test2','test3', 'test4','test5','test6'], 
        #max_height=5, 
        slow_scroll=True, scroll_exit=True)
    SA.display()
    w.edit()
    w.display()
    curses.napms(2000)
    w.clear(usechar='*')
    SA.refresh()
    curses.beep()
    curses.napms(2000)
    return "%s %s" % (str(w.height),  str(w.width))

if __name__ == '__main__':
    import curses.wrapper
    print(curses.wrapper(testme))
    print("No, I'll never join you")


## MultiLineTree

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
    print(curses.wrapper(testme))
    print("No, I'll never join you")


## MultiSelect

def simpletest(screen):
    import screen_area
    SA = screen_area.ScreenArea()
    w = TitleMultiSelect(SA, name="Title Multi", values = ["line 1", "line 2", "line 3", "line 4", "line 5"], max_height=4)
    w.value = [1, 2]
    w.edit()
    w.update()
    SA.refresh()
    curses.napms(2000)
    return w.get_selected_objects()
    

if __name__ == "__main__":
    import curses.wrapper
    print(curses.wrapper(simpletest))
    print("The circle is now complete")


## MultiSelectTree

if __name__ == '__main__':

    def testme(sa):
        import screen_area
        import Form
        #SA = screen_area.ScreenArea()

        Tree = NPSTree.NPSTreeData(content = "Test",)
        n1   = Tree.newChild(content = "TestChild")
        gc1  = n1.newChild(content = "GrandChild1")
        ggc1 = gc1.newChild(content = "Great Grand Child1")
        n2   = Tree.newChild(content = "newChild2")



        SA = Form.Form()
        w = MultiSelectTree(SA, 
            #relx=5, 
            #rely=2, 
            values=Tree, 
            #max_height=5, 
            slow_scroll=True, scroll_exit=False)
        SA.display()
        w.edit()

    import curses.wrapper
    print(curses.wrapper(testme))
    print("No, I'll never join you")


## NewMenuDisplay

def main(*args):
    def setq1():
        global q
        q = 1
    def beep():
        curses.beep()
    def doNothing():
        pass

    q = None   
    M1 = NewMenu.NewMenu(name='Menu1')
    M1.addItem('Beep', beep)
    M1.addItem('Nothing', doNothing)
    M1.addSubmenu(M1)
    
    M2 = NewMenu.NewMenu(name='Menu2')
    M2.addItemsFromList(
        (
            ('Beep', beep),
            ('Nothing', doNothing),
            ('Beep Again', beep),
            M1,)
    )
    
    M1.addSubmenu(M2)
    
    MenuDisplay1 = MenuDisplay()
    MenuDisplay1.setMenu(M1)
    MenuDisplay1.edit()
    return q


if __name__ == '__main__':
    import curses
    q = curses.wrapper(main)
    print(q)
    print("Now I am the Master")


## NPSApplication

if __name__ == '__main__':
    while 1:
     App = NPSApp(); App.run()
     App = NPSApp(); App.run()

    print("A Jedi, who was a pupil of mine...")

## NPSAppManaged

def testmanaged(*args):
     import ActionForm
     import textbox

     class TestForm(ActionForm.ActionForm):
         def afterEditing(self):
             self.parentApp.NEXT_ACTIVE_FORM = None

     T = NPSAppManaged()
     a = T.addForm('MAIN', TestForm, name='Test')
     a.add(textbox.Textfield, name='Test')
     T.main()
     
def main(*args):
    import ActionForm
    import textbox
    
    class TestForm(ActionForm.ActionForm):
        def activate(self):
            self.edit()
            self.parentApp.NEXT_ACTIVE_FORM = None
    
    T = NPSAppManaged()
    a = T.addForm(TestForm, name='Test')
    a.add(textbox.Textfield, name='Test')
    T.registerForm('MAIN', a)
    T.main()


if __name__ == '__main__':
    import curses
    curses.wrapper(testmanaged)

## NPSTree

if __name__ == '__main__':
    def Test1():
        Tree = NPSTreeData(content = "Test",)
        n1   = Tree.newChild(content = "TestChild")
        gc1  = n1.newChild(content = "GrandChild1")
        n2   = Tree.newChild(content = "newChild2")
        for item in Tree.walkTree():
            print('->' * item.findDepth(), item.getContent())
        print(Tree.getTreeAsList())
    
    Test1()

## password

def testloop(sa):
    SA = screen_area.ScreenArea()
    w = TitlePassword(SA)
    w.edit()


if __name__ == "__main__":
    import curses.wrapper
    import screen_area
    curses.wrapper(testloop)
    print("When I wrote you, I had much to learn")

## Popup

def main(*args):
    import titlefield
    import textbox
    import slider
    import multiline
    

    F = Popup(name="Testing")
    w = F.add_widget(titlefield.TitleText)
    str = "useable space = %s, %s; my height and width is: %s, %s" % (F.widget_useable_space()[0], F.widget_useable_space()[1], w.height, w.width)
    w.value = str
    F.nextrely += 1
    s = F.add_widget(slider.Slider, out_of=10)
    F.edit()

def MessageTest(*args):
    F = MessagePopup()
    F.TextWidget.values = ["This is a ", "very quick test", "of a very useful", "widget", "One","Two","Three","Four","Five"]
    F.edit()

if __name__ == '__main__':
    import curses.wrapper
    from Form import *
    curses.wrapper(MessageTest)

## Screen Area

def test_loop(screen):
    while 1:
        A = ScreenArea()
        A.refresh()
    
    


if __name__ == '__main__':
    curses.wrapper(test_loop)
    print("The circle is now complete")



## Slider

def testme(sa):
    import screen_area
    SA = screen_area.ScreenArea()
    w = TitleSlider(SA, rely = 10, relx=5)
    w.edit()
    w.display()
    curses.napms(1500)


if __name__ == '__main__':
    import curses.wrapper
    curses.wrapper(testme)
    print("Only now...do you see the truth")


## Textbox

def cleartest(screen):
    import screen_area
    SA = screen_area.ScreenArea()
    w  = Textfield(SA, rely=1, relx=3)
    w.value = "This is some text! height: %s, width %s." % (w.height, w.width)
    w.display()
    curses.napms(1000)
    curses.beep()
    w.clear()
    SA.refresh()
    curses.napms(2000)
    
def simpletest(screen):
    import screen_area
    SA = screen_area.ScreenArea()
    w = Textfield(SA, rely=23, relx=6, width=15)
    w.value = "height: %s, width %s" % (w.height, w.width)
    w.edit()
    w.update()
    w2 = Textfield(SA, rely=20, relx=6, width=15)
    w.clear(usechar='x')
    w2.clear(usechar='x')
    SA.refresh()
    curses.napms(2000)

def unicodetest(screen):
    import screen_area
    SA = screen_area.ScreenArea()
    w = Textfield(SA,rely=2, relx=2)
    w.value = u'\u00c5 even this'
    #w.value = 'even this'
    w.edit()
    

if __name__ == "__main__":
    import locale
    import safewrapper
    safewrapper.wrapper(unicodetest)
    print(locale.getlocale()[1])
    print("The circle is now complete")


## Textbox_ControlChars

def simpletest(screen):
    import screen_area
    SA = screen_area.ScreenArea()
    w = TextfieldCtrlChars(SA, rely=23, relx=66)
    w.value = "height: %s, width %s" % (w.height, w.width)
    w.edit()
    w.update()
    SA.refresh()
    curses.napms(2000)


if __name__ == "__main__":
    curses.wrapper(simpletest)
    print("The circle is now complete")

## titlefield

def testloop(sa):
    import screen_area
    SA = screen_area.ScreenArea()
    w = TitleText(SA, use_two_lines=True, rely = 23, value="testing")
    w.value = 'this is a new test'
    w.edit()
    curses.napms(2500)

def cleartest(screen):
    import screen_area
    SA = screen_area.ScreenArea()
    w  = TitleText(SA, name="Test", rely=1, relx=3)
    w.value = "This is some text! height: %s, width %s" % (w.height, w.width)
    w.display()
    curses.napms(1000)
    curses.beep()
    w.clear()
    SA.refresh()
    curses.napms(2000)




if __name__ == '__main__':
    import curses.wrapper
    curses.wrapper(cleartest)
    print("The circle is now complete")


## widget

def simpletest(scr):
    import screen_area as sa
    a = sa.ScreenArea()
    b = Widget(a)
    return b.safe_string(u'Q \u00c5 \u00c5 This\nis something of a test\nThis is line2')


if __name__ == "__main__":
    import safewrapper
    print(safewrapper.wrapper(simpletest))
    print(locale.getlocale()[1])
    print("The circle is now complete")
