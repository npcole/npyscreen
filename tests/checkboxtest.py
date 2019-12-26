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
