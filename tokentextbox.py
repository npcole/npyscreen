#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: npsapp.py
import cProfile
import pstats

from npyscreen import NPSApp
from npyscreen import Form
from npyscreen import TextTokens, TitleTextTokens

class TextBoxForm(Form):
    def create(self):
        tb = self.add(TextTokens, name="TokenField", )#max_width=25)
        tb.value = [
                    "Token 1 Testing", 
                    "Token 2 ééé", 
                    "Token 3 ", 
                    "Token 4 ",
                    "Token 6 ",
                    "Token 7 ",
                    "Token 8 ",
                    "Token 9 ",
                    "Token 10 ",
                    "Token 11 ",
                    "Token 12 ",
                    "Token 6b ",
                    "Token 7b ",
                    "Token 8b ",
                    "Token 9b ",
                    "Token 10b ",
                    "Token 11b ",
                    "Token 12b ",
                    ]
        #tb.begin_at += 0
        #tb.important=True
        #tb.show_bold=True
        self.highlight=True
        tb.cursor_position=3
        tb.left_margin=8





class App(NPSApp):
   def main(self):
       form = TextBoxForm(name='Welcome to Npyscreen')
       form.edit()

if __name__ == '__main__':
   app = App()
   p = cProfile.run('app.run()', sort=1)
