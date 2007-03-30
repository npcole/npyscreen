#!/usr/bin/python
# encoding: utf-8


import sys
import os
import multiline
import Form
import weakref


class MenuScreen(object):
	def __init__(self, name=None, show_atx=None, show_aty=None):
		self.__menu_items = []
		self.name = name
		self.__show_atx = show_atx
		self.__show_aty = show_aty
		
	def add_item(self, text, func, shortcut=None):
		self.__menu_items.append((text, func, shortcut))
	
	def set_menu(self, pairs):
		"""Pass in a list of pairs of text labels and functions"""
		self.__menu_items = []
		for pair in pairs:
			self.add_item(pair[0], pair[1])
