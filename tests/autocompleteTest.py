def testme(scr):
    import Form
    F = Form.Form()
    w = F.add(TitleFilename, name="Filename")
    F.edit()

if __name__ == '__main__':
    import curses
    curses.wrapper(testme)
