#!/usr/bin/python
import curses
import npyscreen
import unittest

npyscreen.add_test_input_from_iterable('This is a test')
npyscreen.TEST_SETTINGS['TEST_INPUT'].append(curses.KEY_DOWN)
npyscreen.TEST_SETTINGS['TEST_INPUT'].append("^X")
npyscreen.TEST_SETTINGS['CONTINUE_AFTER_TEST_INPUT'] = True

class TestForm(npyscreen.FormWithMenus):
    def create(self):
        self.myTitleText = self.add(npyscreen.TitleText, name="Events (Form Controlled):", editable=True)

class TestApp(npyscreen.StandardApp):
    def onStart(self):
        self.addForm("MAIN", TestForm)

class Tests(unittest.TestCase):
    def setUp(self):
        self.testApp = TestApp()
        
    def test_text_entry(self):
        npyscreen.TEST_SETTINGS['TEST_INPUT'] = [ch for ch in 'This is a test']
        npyscreen.TEST_SETTINGS['TEST_INPUT'].append(curses.KEY_DOWN)
        
        
        

if __name__ == '__main__':
    #TestMemory()
    A = TestApp()
    A.run()