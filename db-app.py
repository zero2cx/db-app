#!/usr/bin/env python
# db-app.py v0.1

# Display a GUI that administers records in an Sqlite database table.
#   Project home: <https://github.com/zero2cx/the-python-mega-course>
#   Copyright (C) 2017 David Schenck
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import tkinter as tk
from lib.db import Database
from lib.seed import seed_database

################################################################################
### TODO: add an option to specify column names on the command-line, when using a seed file.
class AppInterface():
    """
    AppInterface parses arguments from the command-line and responds there,
    if necessary.
    """
    def __init__(self):
        """Start with generic values, to be updated from command-line args."""
        self.seed = False
        self.title = 'Database Control Interface'
        self.db_path = '%s/data' % \
                (os.path.dirname(p=os.path.abspath(path=__file__)))
        self.db_name = None

    def parse_args(self, args):
        """
        Parse command-line arguments and set instance variables for the app.
        """
        while args:
            """Show the help message text for the app."""
            if args[0] == '-h' or args[0] == '--help':
                self.show_usage(status=0)
            """Flags a requirement to populate the database with some initial
            seed data. Seed data will be read from the file '<db_name>.csv'."""
            if args[0] == '-s' or args[0] == '--seed':
                self.seed = True
                args.pop(0)
                continue
            """The title text for the user-interface window."""
            if args[0] == '-t' or args[0] == '--title':
                args.pop(0)
                if args:
                    self.title = args[0]
                    args.pop(0)
                continue
            """The directory path to the database or seed file."""
            if args[0] == '-p' or args[0] == '--path':
                args.pop(0)
                if args:
                    self.db_path = args[0]
                    args.pop(0)
                continue
            """The base filename of the database file (<db_name>.db) or seed
            file (<db_name>.csv)."""
            if not self.db_name:
                self.db_name = args[0]
                args.pop(0)
            else:
                """The current arg didn't parse as a valid option, and db_name
                has already been parsed above, so the current arg is invalid."""
                self.show_usage('**Error: %s' % ('incorrect usage'))
        """Validity-check the instance variables. Quit if invalid."""
        if self.db_path[0] == '.':
            self.db_path = '%s/%s' % (os.getcwd(), self.db_path)
        db_file = os.path.normpath('%s/%s.db' % (self.db_path, self.db_name))
        seed_file = os.path.normpath('%s/%s.csv' % (self.db_path, self.db_name))
        if not self.db_name:
            msg = '**Error: %s' % ('database name not specified')
            self.show_usage(msg)
        if not os.path.isdir(self.db_path):
            msg = '**Error: %s, "%s"' % ('directory not found', self.db_path)
            self.show_usage(msg)
        if self.seed and not os.path.isfile(seed_file):
            msg = '**Error: %s, "%s"' % ('seed file not found', seed_file)
            self.show_usage(msg)
        if not self.seed and not os.path.isfile(db_file):
            msg = '**Error: %s, "%s"' % ('database file not found', db_file)
            self.show_usage(msg)

    def show_usage(self, status):
        """
        Display usage text to the command line interface, and then exit.
        """
        script = os.path.basename(__file__)     # script = sys.argv[0][sys.argv[0].rfind('/')+1:]
        print("""
Usage: %s [--seed] [--title TITLE] [--path DIRECTORY] DB_NAME
       %s --help

   Options:
        -s | --seed             Initialize a fresh database from seed data.
        -t | --title TITLE      Specify a TITLE for the GUI window.
        -p | --path DIRECTORY   Specify a DIRECTORY for the database file.
        -h | --help             Print this message text.

    This app displays a database-control interface for an Sqlite database named
    <DB_NAME>. That database's file name will be '<DB_NAME>.db'. The database
    file location defaults to the application sub-directory named 'data'. The
    non-extensive user interface is able to administer a database that contains
    just one table, and that table's name duplicates the database's name.
    i.e. Table 'books' in database 'books.db'.

    When the '--seed' option is specified, then the database-table's column
    names, as well as the table's contents, are generated from the comma-
    seperated file which corresponds to <DB_NAME> with a filename extension
    '.csv' appended, i.e. '<DB_NAME>.csv'. When using seed data from such a
    file, the database file will be created within the same directory as where
    the seed file is located.

    When the '--path' option is specified, then <DIRECTORY> is used in place of
    the default directiory as the location for the database file and (when used)
    the seed file.

    When the '--title' option is specified, then <TITLE> is displayed as the
    database-control interface's window title.

    When using seed data, the seed file's contents should consist of newline-
    seperated data records. In addition, the database-table's column data will
    correspond to the comma-seperated fields within each line of the seed file.
    The first line in the seed file will specify the database-table's column
    names, also comma-seperated.
        """ % (script, script))
        sys.exit(status)

################################################################################
class UserInterface():
    """
    UserInterface creates and places Tk form elements according to the caller's
    specification. These elements consists of a flexible count of entry elements
    with associated label elements, a listbox element with scrollbar attached,
    and buttons that interface with whichever database is associated with the
    caller.
    """
    def __init__(self, window, fields, buttons):
        self.fields = fields
        self.window = window
        self.lbl = {}
        self.ent = {}
        self.btn = {}
        self.lst = None
        self.selected = None
        self.col = 0
        self.row = 0
        """Add the data-entry fields, a listbox with scrollbar, and the buttons
        to the user interface."""
        for field in fields:
            self.add_field(name=field, field_break=2)
        self.add_list()
        for i in range(len(buttons)):
            self.add_button(name=buttons[i][0], command=buttons[i][1])

    def add_field(self, name, field_break=2):
        """Add a label element for the field."""
        text = '%s: ' % (name.replace('_', ' ').title())
        label = tk.Label(master=self.window, text=text, height=2, width=12,
                         anchor=tk.E)
        label.grid(row=self.row, column=self.col)
        self.col += 1
        """Add an entry element for the field."""
        entry = tk.Entry(master=self.window, textvariable=tk.StringVar(),
                         width=16)
        entry.grid(row=self.row, column=self.col)
        self.col += 1
        """Return to column 0 of the next row, if the field-break has been
        encountered. The field-break limits the continued horizontal placement
        of new fields within the current row."""
        if self.col > (field_break - 1) * 2:
            self.col = 0
            self.row += 1
        self.lbl[name] = label
        self.ent[name] = entry

    def add_list(self):
        self.row += 1
        self.col = 0
        """Add a listbox element."""
        listbox = tk.Listbox(master=self.window, width=28)
        listbox.grid(row=self.row, column=self.col, rowspan=6, columnspan=2,
                 sticky=tk.E)
        self.col += 2
        """Add a scrollbar element."""
        scrollbar = tk.Scrollbar(master=self.window)
        scrollbar.grid(row=self.row, column=self.col, rowspan=6, sticky=tk.W)
        """Link the listbox with the scrollbar, and vice-verse. Bind to a click
        event within the listbox."""
        listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=listbox.yview)
        listbox.bind(sequence='<<ListboxSelect>>', func=self.get_selected)
        self.col += 1
        self.lst = listbox

    def add_button(self, name, command):
        """Add a button element."""
        name = name.replace('_', ' ').title()
        button = tk.Button(master=self.window, text=name, width='12',
                           command=command)
        button.grid(row=self.row, column=self.col, sticky=tk.E)
        self.row += 1
        self.btn[name] = button

    def get_selected(self, event):
        """Determine which member in the listbox has been clicked, if any."""
        try:
            i = 0
            index = self.lst.curselection()[i]
            self.selected = self.lst.get(index)
            """Populate the entry elements with the selected member's data."""
            for field in self.fields:
                i += 1
                self.ent[field].delete(0, tk.END)
                self.ent[field].insert(tk.END, self.selected[i])
        except IndexError:
            return

################################################################################
class Window():
    """
    Window generates a GUI interface via the UserInterface class and interfaces
    with an Sqlite database via the Database class.
    """
    def __init__(self, window, title, db):
        self.window = window
        self.window.wm_title(string=title)
        self.db = db
        """Build the data-entry field list from the database-table column
        names."""
        fields = []
        for column in self.db.get_column_names():
            fields.append(column)
        """Build the button element list."""
        buttons = [
            ('view_all', self.view_collection),
            ('search', self.search_collection),
            ('add_new', self.add_item),
            ('update', self.update_item),
            ('delete', self.delete_item),
            ('close', self.window.quit)
        ]
        """Initialize the user interface."""
        self.ui = UserInterface(self.window, fields, buttons)
        self.view_collection()

    def view_collection(self):
        """Display all records in the database table."""
        self.ui.lst.delete(0, tk.END)
        for record in self.db.get_all_records():
            self.ui.lst.insert(tk.END, record)

    def search_collection(self):
        """From the database table, search for all records that conform to
        specified search criteria."""
        val = {}
        for name in self.db.get_column_names():
            val[name] = self.ui.ent[name].get()
        records = self.db.get_records(**val)
        self.ui.lst.delete(0, tk.END)
        for record in records:
            self.ui.lst.insert(tk.END, (record))

    def add_item(self):
        """Add a record to the database table."""
        record = []
        for name in self.db.get_column_names():
            field = self.ui.ent[name].get()
            if not field:
                return
            record.append(field)
        self.db.add_record(record=record)
        self.view_collection()

    def update_item(self):
        """Update with changes a record in the database table."""
        try:
            id = self.ui.selected[0]
        except NameError:
            return
        val = {}
        for name in self.db.get_column_names():
            val[name] = self.ui.ent[name].get()
            if not val[name]:
                return
        self.db.update_record(id=id, **val)
        self.view_collection()

    def delete_item(self):
        """Delete a record from the database table."""
        try:
            id = self.ui.selected[0]
        except NameError:
            return
        self.db.delete_record(id)
        self.view_collection()

################################################################################
app = AppInterface()
app.parse_args(args=sys.argv[1:])
if app.seed:
    seed_database(path=app.db_path, name=app.db_name)
app.window = tk.Tk()
Window(window=app.window, title=app.title,
        db=Database(path=app.db_path, name=app.db_name))
app.window.mainloop()
