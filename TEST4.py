import npyscreen
import curses


class TestForm(npyscreen.Form):

    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def create(self):
        self.grid = self.add(npyscreen.GridColTitles, name='GRID',
column_width=10, values=[(1, 2, 3, 4), (10, 20, 30, 40)], col_titles=['A',
'B', 'C', 'D'])
        self.grid.when_cursor_moved = curses.beep


class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', TestForm, name='Test Form')


if __name__ == '__main__':
    TestApp = MyApplication().run()

