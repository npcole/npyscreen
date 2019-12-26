def testme(sa):
    import screen_area
    SA = screen_area.ScreenArea()
    w = MiniButton(SA, rely=3, relx=3)
    w.edit()
    w.display()
    curses.napms(1500)


if __name__ == '__main__':
    import curses.wrapper
    curses.wrapper(testme)
    print("Join me, and we will end this destructive conflict")
