# -*- coding: utf-8 -*-
# filename: npsapp.py

from npyscreen import NPSApp
from npyscreen import Form

class App(NPSApp):
   def main(self):
       form = Form(name='Welcome to Npyscreen')
       form.edit()

if __name__ == '__main__':
   app = App()
   app.run()

