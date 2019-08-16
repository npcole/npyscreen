import npyscreen
import curses



class TestTitleText(widget.Widget):
    _entry_type = textbox.Textfield



class TestTitleWidget(npyscreen.TitleText):
    def set_up_handlers(self):
        self.handlers = {
                   curses.ascii.NL:     self.h_exit_down,
                   curses.ascii.CR:     self.h_exit_down,
                   curses.ascii.TAB:    self.h_exit_down,
                   curses.KEY_BTAB:     self.h_exit_up,
                   curses.KEY_DOWN:     self.h_exit_down,
                   curses.KEY_UP:       self.h_exit_up,
                   curses.KEY_LEFT:     self.h_exit_left,
        }
    
    def h_exit_down(self, h):
        self.exit_up()



def TitleTest(screen):
    F = npyscreen.Form()
    F.add(TestTitleWidget, name="Title 1")
    F.add(TestTitleWidget, name="Title 2")
    F.edit()



if __name__ == "__main__":
	curses.wrapper(TitleTest)