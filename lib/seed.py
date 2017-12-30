# seed.py v0.1                                                    -*- Python -*-

# Using a csv-formatted data file, generate a new database-table with seed data.
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
import csv
from .db import Database

### TODO: extend flexibility for using a variety of seed data field-seperators.
### TODO: maybe could write a data pre-processor to standardize sloppy seed data. DIFFICULT!!!
### TODO: add web-scraping as a source of seed data.
def seed_database(path, name):
    """
    Read the contents of a csv-formatted file containing seed data for an Sqlite
    database-table. Then populate an Sqlite database and save to file. If a file
    already exists, then do a destructive overwrite with the new database file.
    """
    """Fetch the seed data including column names from the seed file."""
    column_names, records = _get_seed_data('%s/%s.csv' % (path, name))
    if not column_names:
        return 1
    """Parse each data record, and designate the appropriate data type for each
    table column."""
    columns = dict(zip(column_names, _get_column_types(records=records)))
    """Delete the old database file, if exists."""
    db_file = os.path.normpath('%s/%s.db' % (path, name))
    if os.path.isfile(path=db_file):
        os.remove(db_file)
    """Create and connect to an empty database file. Add seed data to it, then
    close the connection."""
    db = Database(path=path, name=name, **columns)
    for record in records:
        db.add_record(record=record)
    db.close()

def _get_seed_data(seed_file):
    """
    Read a csv-formatted file and return the contents as two lists. A list of
    database-table column names, and a list of data records of type list.
    """
    rows = []
    with open(file=seed_file, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
    return rows.pop(0), rows

def _get_column_types(records):
    """Build a list of lists that makes note of the data type of each field
    within each data record."""
    data_types = []
    for i in range(len(records[0])):
        data_types.append([])
    for record in records:
        for i in range(len(data_types)):
            try:
                int(record[i])
            except ValueError:
                try:
                    float(record[i])
                except:
                    data_types[i].append('TEXT')
                else:
                    data_types[i].append('REAL')
            else:
                data_types[i].append('INTEGER')
    """Assign types to the table columns to match the parsed data types from the
    above list-of-lists."""
    column_types = []
    for i in range(len(data_types)):
        if 'REAL' in data_types[i]:
            column_types.append('REAL')
        elif 'INTEGER' in data_types[i]:
            column_types.append('INTEGER')
        else:
            column_types.append('TEXT')
    return column_types
