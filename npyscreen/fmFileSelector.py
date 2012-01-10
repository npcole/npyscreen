from . import fmFormMutt
from . import wgmultiline
from . import wggrid
from . import wgautocomplete

import curses
import os
import os.path
import operator

class FileCommand(wgautocomplete.Filename):
    def set_up_handlers(self):
        super(FileCommand, self).set_up_handlers()
        self.handlers.update ({
            curses.ascii.NL:    self.h_select_file,
        })
        
    def h_select_file(self, *args, **keywords):
        self.h_exit_down(None)
        self.parent.exit_editing()
        
    def auto_complete(self, input):
        self.value = os.path.expanduser(self.value)
        
        for i in range(1):
            dir, fname = os.path.split(self.value)
            # Let's have absolute paths.
            dir = os.path.abspath(dir)
            
            if self.value == '': 
                self.value=dir
                break
            
            try: 
                flist = os.listdir(dir)
            except:
                self.show_brief_message("Can't read directory!")
                break

            flist = [os.path.join(dir, x) for x in flist]
            possibilities = list(filter(
                (lambda x: os.path.split(x)[1].startswith(fname)), flist
                ))

            if len(possibilities) is 0:
                # can't complete
                curses.beep()
                break

            if len(possibilities) is 1:
                if self.value != possibilities[0]:
                    self.value = possibilities[0]
                    if os.path.isdir(self.value) \
                        and not self.value.endswith(os.sep):
                        self.value = self.value + os.sep
                    break
        
        if os.path.isdir(self.value):
            self.parent.value = self.value
            self.parent.update_grid()
            self.h_exit_up(None)
        else:
            self.parent.value = dir
            self.parent.update_grid()


class FileGrid(wggrid.SimpleGrid):
    default_column_number = 3
    
    def set_up_handlers(self):
        super(FileGrid, self).set_up_handlers()
        self.handlers.update ({
            curses.ascii.NL:    self.h_select_file,
            curses.ascii.SP:    self.h_select_file,
        })
    
    def h_select_file(self, *args, **keywrods):
        try:
             select_file = os.path.join(self.parent.value, self.values[self.edit_cell[0]][self.edit_cell[1]])
             select_file = os.path.abspath(select_file)
        except (TypeError, IndexError):
            self.edit_cell = [0, 0]
            return False
        
        if os.path.isdir(select_file):
            self.parent.value = select_file
            self.parent.wCommand.value = select_file
            self.parent.update_grid()
            self.edit_cell = [0, 0]
            
        else:
            self.parent.wCommand.value = select_file
            self.h_exit_down(None)
    
    def display_value(self, vl):
        p = os.path.split(vl)
        if p[1]:
            return p[1]
        else:
            return os.path.split(p[0])[1] + os.sep
        
class FileSelector(fmFormMutt.FormMutt):
    MAIN_WIDGET_CLASS   = FileGrid
    COMMAND_WIDGET_CLASS= FileCommand
    def __init__(self, 
        select_dir=False, #Select a dir, not a file
        must_exist=False, #Selected File must already exist
        *args, **keywords):
        self.select_dir = select_dir
        self.must_exist = must_exist
        
        super(FileSelector, self).__init__(*args, **keywords)
        try:
            if not self.value:
                self.value = os.getcwd()
        except:
            self.value = os.getcwd()
    
    def beforeEditing(self,):
        self.adjust_widgets()
    
    def update_grid(self,):
        if self.value:
            self.value = os.path.expanduser(self.value)
        
        if not os.path.exists(self.value):
            self.value = os.getcwd()
            
        if os.path.isdir(self.value):
            working_dir = self.value
        else:
            working_dir = os.path.dirname(self.value)
            
        self.wStatus1.value = working_dir
        
        file_list = [".." ]
        file_list.extend([os.path.join(working_dir, fn) for fn in os.listdir(working_dir)])

        # DOES NOT CURRENTLY WORK - EXCEPT FOR THE WORKING DIRECTORY.  REFACTOR.
        new_file_list= []
        for f in file_list:
            f = os.path.normpath(f)
            if os.path.isdir(f):
                new_file_list.append(f + os.sep)
            else:
                new_file_list.append(f) # + "*")
        file_list = new_file_list
        del new_file_list

        # sort Filelist
        file_list.sort()
        file_list.sort(key=os.path.isdir, reverse=True)
        
                
        file_list_cols    = [ [], ]
        column_number_max = self.wMain.columns
        col_number        = 0
        row_number        = 0
        for f in file_list:
            if col_number >= column_number_max:
                col_number = 0
                file_list_cols.append([])
                row_number += 1
            file_list_cols[row_number].append(f)    
            col_number += 1
        
        self.wMain.values = file_list_cols
        self.edit_cell = [0,0]
        self.display()
        
    def adjust_widgets(self):
        self.update_grid()
        