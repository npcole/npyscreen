Example Application: A simple address book
===========================================

An address book applicaton requires a database.  For the sake of convenience, we will use sqlite. ::

    class AddressDatabase(object):
        def __init__(self, filename="example-addressbook.db"):
            self.dbfilename = filename
            db = sqlite3.connect(self.dbfilename)
            c = db.cursor()
            c.execute(
            "CREATE TABLE IF NOT EXISTS records\
                ( record_internal_id INTEGER PRIMARY KEY, \
                  last_name     TEXT, \
                  other_names   TEXT, \
                  email_address TEXT \
                  )" \
                )
            db.commit()
            c.close()    
    
        def add_record(self, last_name = '', other_names='', email_address=''):
            db = sqlite3.connect(self.dbfilename)
            c = db.cursor()
            c.execute('INSERT INTO records(last_name, other_names, email_address) \
                        VALUES(?,?,?)', (last_name, other_names, email_address))
            db.commit()
            c.close()
    
        def update_record(self, record_id, last_name = '', other_names='', email_address=''):
            db = sqlite3.connect(self.dbfilename)
            c = db.cursor()
            c.execute('UPDATE records set last_name=?, other_names=?, email_address=? \
                        WHERE record_internal_id=?', (last_name, other_names, email_address, \
                                                            record_id))
            db.commit()
            c.close()    

        def delete_record(self, record_id):
            db = sqlite3.connect(self.dbfilename)
            c = db.cursor()
            c.execute('DELETE FROM records where record_internal_id=?', (record_id,))
            db.commit()
            c.close()    
    
        def list_all_records(self, ):
            db = sqlite3.connect(self.dbfilename)
            c = db.cursor()
            c.execute('SELECT * from records')
            records = c.fetchall()
            c.close()
            return records
    
        def get_record(self, record_id):
            db = sqlite3.connect(self.dbfilename)
            c = db.cursor()
            c.execute('SELECT * from records WHERE record_internal_id=?', (record_id,))
            records = c.fetchall()
            c.close()
            return records[0]

The main screen of the application will be a list of names.  When the user selects a name, we will want to edit it.  We will subclass MultiLineAction, and override `display value` to change how each record is presented.  We will also override the method `actionHighlighted` to switch to the edit form when required.  Finally, we will add two new keypresses - one to add and one to delete records.  Before switching to the EDITRECORDFM, we either set its value to None, if creating a new form, or else set its value to that of the record we wish to edit. ::
    
    class RecordList(npyscreen.MultiLineAction):
        def __init__(self, *args, **keywords):
            super(RecordList, self).__init__(*args, **keywords)
            self.add_handlers({
                "^A": self.when_add_record,
                "^D": self.when_delete_record
            })

        def display_value(self, vl):
            return "%s, %s" % (vl[1], vl[2])
    
        def actionHighlighted(self, act_on_this, keypress):
            self.parent.parentApp.getForm('EDITRECORDFM').value =act_on_this[0]
            self.parent.parentApp.switchForm('EDITRECORDFM')

        def when_add_record(self, *args, **keywords):
            self.parent.parentApp.getForm('EDITRECORDFM').value = None
            self.parent.parentApp.switchForm('EDITRECORDFM')
    
        def when_delete_record(self, *args, **keywords):
            self.parent.parentApp.myDatabase.delete_record(self.values[self.cursor_line][0])
            self.parent.update_list()
            
The actual form to display the record list will be a FormMutt subclass. We will alter the `MAIN_WIDGET_CLASS` class variable to use our RecordList widget, and make sure that the list of records is updated every time the form is presented to the user. ::

    class RecordListDisplay(npyscreen.FormMutt):
        MAIN_WIDGET_CLASS = RecordList
        def beforeEditing(self):
            self.update_list()
    
        def update_list(self):
            self.wMain.values = self.parentApp.myDatabase.list_all_records()
            self.wMain.display()

The form to edit each record will be an example of an ActionForm.  Records will only be altered when the user selects the 'ok' button. Before the form is presented to the user, the values of each of the individual widgets are updated to match the database record, or cleared if we are creating a new record. ::

    class EditRecord(npyscreen.ActionForm):
        def create(self):
            self.value = None
            self.wgLastName   = self.add(npyscreen.TitleText, name = "Last Name:",)
            self.wgOtherNames = self.add(npyscreen.TitleText, name = "Other Names:")
            self.wgEmail      = self.add(npyscreen.TitleText, name = "Email:")
        
        def beforeEditing(self):
            if self.value:
                record = self.parentApp.myDatabase.get_record(self.value)
                self.name = "Record id : %s" % record[0]
                self.record_id          = record[0]
                self.wgLastName.value   = record[1]
                self.wgOtherNames.value = record[2]
                self.wgEmail.value      = record[3]
            else:
                self.name = "New Record"
                self.record_id          = ''
                self.wgLastName.value   = ''
                self.wgOtherNames.value = ''
                self.wgEmail.value      = ''
    
        def on_ok(self):
            if self.record_id: # We are editing an existing record
                self.parentApp.myDatabase.update_record(self.record_id,
                                                last_name=self.wgLastName.value,
                                                other_names = self.wgOtherNames.value,
                                                email_address = self.wgEmail.value,
                                                )
            else: # We are adding a new record.
                self.parentApp.myDatabase.add_record(last_name=self.wgLastName.value,
                other_names = self.wgOtherNames.value,
                email_address = self.wgEmail.value,
                )
            self.parentApp.switchFormPrevious()
    
        def on_cancel(self):
            self.parentApp.switchFormPrevious()

Finally, we need an application object that manages the two forms and the database::

    class AddressBookApplication(npyscreen.NPSAppManaged):
        def onStart(self):
            self.myDatabase = AddressDatabase()
            self.addForm("MAIN", RecordListDisplay)
            self.addForm("EDITRECORDFM", EditRecord)
    
    if __name__ == '__main__':
        myApp = AddressBookApplication()
        myApp.run() 