#!/usr/bin/env python

from . import wgwidget   as widget
import calendar
import datetime
import curses

class DateEntryBase(widget.Widget):
    def __init__(self, screen, allowPastDate=True, allowTodaysDate=True, firstWeekDay=6, **keywords):
        super(DateEntryBase, self).__init__(screen, **keywords)
        self.allow_date_in_past = allowPastDate
        self.allow_todays_date  = allowTodaysDate
        self._max = datetime.date.max
        self._min = datetime.date.min
        self.firstWeekDay = firstWeekDay
        

    def _check_date(self):
        if not self.allow_date_in_past:
            if self.value < datetime.date.today():
                if self.allow_todays_date:
                    self.value = datetime.date.today()
                else:
                    self.value = datetime.date.today() + datetime.timedelta(1)      
        
    def _check_today_validity(self, onErrorHigher=True):
        """If not allowed to select today's date, and today is selected, move either higher or lower
depending on the value of onErrorHigher"""
        if not self.allow_date_in_past:
            onErrorHigher = True
        if self.allow_todays_date:
            return True
        else:
            if self.value == datetime.date.today():
                if onErrorHigher:
                    self.value += datetime.timedelta(1)
                else:
                    self.value -= datetime.timedelta(1)
    
    
    def set_up_handlers(self):
        super(DateEntryBase, self).set_up_handlers()
        self.handlers.update({ "D":    self.h_day_less,
                               "d":    self.h_day_more,
                               "W":    self.h_week_less,
                               "w":    self.h_week_more,
                               "M":    self.h_month_less,
                               "m":    self.h_month_more,
                               "Y":    self.h_year_less,
                               "y":    self.h_year_more,
                               "t":    self.h_find_today,
                            })
    def _reduce_value_by_delta(self, delta):
        old_value = self.value
        try:
            self.value -= delta
        except:
            self.value = old_value
    
    def _increase_value_by_delta(self, delta):
        old_value = self.value
        try:
            self.value += delta
        except:
            self.value = old_value
    
    
    def h_day_less(self, *args):
        self._reduce_value_by_delta(datetime.timedelta(1))
        self._check_date()
        self._check_today_validity(onErrorHigher=False)

    def h_day_more(self, *args):
        self._increase_value_by_delta(datetime.timedelta(1))
        self._check_date()
        self._check_today_validity(onErrorHigher=True)
    
    def h_week_less(self, *args):
        self._reduce_value_by_delta(datetime.timedelta(7))
        self._check_date()
        self._check_today_validity(onErrorHigher=False)
    
    def h_week_more(self, *args):
        self._increase_value_by_delta(datetime.timedelta(7))
        self._check_date()
        self._check_today_validity(onErrorHigher=True)

    def h_month_less(self, *args):
        self._reduce_value_by_delta(datetime.timedelta(28))
        self._check_date()
        self._check_today_validity(onErrorHigher=False)
    
    def h_month_more(self, *args):
        self._increase_value_by_delta(datetime.timedelta(28))
        self._check_date()
        self._check_today_validity(onErrorHigher=True)

    def h_year_less(self, *args):
        old_value = self.value
        try:
            if self.value.month == 2 and self.value.day == 29:
                self.value = self.value.replace(year=self.value.year-1, day=self.value.day-1)
            else:
                self.value = self.value.replace(year=self.value.year-1)
            self._check_date()
            self._check_today_validity(onErrorHigher=False)
        except:
            self.value=old_value

    def h_year_more(self, *args):
        old_value = self.value
        try:
            if self.value.month == 2 and self.value.day == 29:
                self.value = self.value.replace(year=self.value.year+1, day=self.value.day-1)
            else:
                self.value = self.value.replace(year=self.value.year+1)
            self._check_date()
            self._check_today_validity(onErrorHigher=True)
        except:
            self.value = old_value
            
    def h_find_today(self, *args):
        self.value = datetime.date.today()  
        self._check_date()
        self._check_today_validity(onErrorHigher=True)

class MonthBox(DateEntryBase):
    DAY_FIELD_WIDTH = 4
    
    def __init__(self, screen, **keywords):
        super(MonthBox, self).__init__(screen, **keywords)
        
    def calculate_area_needed(self):
        # Rember that although months only have 4-5 weeks, they can span 6 weeks.
        # Currently allowing 2 lines for headers, so 8 lines total
        return 10, self.__class__.DAY_FIELD_WIDTH * 7
    
    def update(self, clear=True):
        calendar.setfirstweekday(self.firstWeekDay)
        if clear: self.clear()
        if self.hidden:
            self.clear()
            return False
        if not self.value:
            self.addstr(self.rely, self.relx, "No value set")
        else:
            year  = self.value.year
            month = self.value.month
            monthname = self.value.strftime('%B')
            day   = self.value.day
        
            # Print the Title Line
            if self.do_colors():
                self.parent.curses_pad.addstr(self.rely, self.relx, ("%s, %s" % (monthname, year)), 
                                                    self.parent.theme_manager.findPair(self))
            else:
                self.parent.curses_pad.addstr(self.rely, self.relx, ("%s, %s" % (monthname, year)))
        
            # Print the day names
            # weekheader puts an extra space at the end of each name
            if self.do_colors():
                self.parent.curses_pad.addstr(self.rely+1, self.relx, calendar.weekheader(self.__class__.DAY_FIELD_WIDTH - 1),
                                                self.parent.theme_manager.findPair(self, 'LABEL'))
            else:
                self.parent.curses_pad.addstr(self.rely+1, self.relx, calendar.weekheader(self.__class__.DAY_FIELD_WIDTH - 1))
        
            # Print the days themselves
            cal_data = calendar.monthcalendar(year, month)
            print_line = self.rely+2
        
            for calrow in cal_data:
                print_column = self.relx
            
                for thisday in calrow:
                    if thisday is 0:
                        pass
                    elif day == thisday:
                        if self.do_colors():
                            self.parent.curses_pad.addstr(print_line, print_column, str(thisday), curses.A_STANDOUT | self.parent.theme_manager.findPair(self, self.color))
                        else:
                            self.parent.curses_pad.addstr(print_line, print_column, str(thisday), curses.A_STANDOUT)
                    else:
                        if self.do_colors():
                            self.parent.curses_pad.addstr(print_line, print_column, str(thisday), self.parent.theme_manager.findPair(self, self.color))
                        else:
                            self.parent.curses_pad.addstr(print_line, print_column, str(thisday))
                    print_column += self.__class__.DAY_FIELD_WIDTH
            
                print_line += 1
            # Print some help
            if self.do_colors():
                self.parent.curses_pad.addstr(self.rely+9, self.relx, "keys: dwmyDWMYt", self.parent.theme_manager.findPair(self, 'LABEL'))
            else:
                self.parent.curses_pad.addstr(self.rely+9, self.relx, "keys: dwmyDWMYt")

        
    def set_up_handlers(self):
        super(MonthBox, self).set_up_handlers()
        self.handlers.update({curses.KEY_LEFT:    self.h_day_less,
                              curses.KEY_RIGHT:   self.h_day_more,
                              curses.KEY_UP:      self.h_week_less,
                              curses.KEY_DOWN:    self.h_week_more,
                              curses.ascii.SP:    self.h_exit_down,
                              "^T":               self.h_find_today,
                            })

