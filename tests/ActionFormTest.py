def testme(sa):
    import titlefield
    import textbox
    import slider
    import multiline

    F = ActionForm(name="Testing Action Form")
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
    import curses
    curses.wrapper(testme)
    print("No Luke, I am your father")
