# db.py v0.1                                                      -*- Python -*-

# Provide sqlite database functionality for frontend script(s).
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

import sqlite3

################################################################################
### TODO: add the capacity to manage multiple database tables and sensibly switch between them.
class Database():
    """
    Database opens a connection to an existing database, or instead create a
    new, empty database and connects to that. When a dictionary of column names
    and types is passed upon instantiation, and if a table does not exist in the
    database, then a new, empty table is created. The database that is created
    consists of one table that duplicates the name of the database itself.
    """
    def __init__(self, path, name, **kwargs):
        self.file = '%s/%s.db' % (path, name)
        self.table = name
        self.conn = sqlite3.connect(database=self.file)
        self.curs = self.conn.cursor()
        if kwargs:
            sql = 'CREATE TABLE IF NOT EXISTS %s (id INTEGER PRIMARY KEY' % \
                    (self.table)
            for key in kwargs:
                sql += ', %s %s' % (key.lower(), kwargs[key])
            sql += ')'
            print(sql)
            self.curs.execute(sql)
            self.conn.commit()

    def __del__(self):
        """Close the database connection."""
        self.close()

    def get_column_names(self, pkey=False):
        """
        Return a list of the table's column names. The table's primary key is
        not included, by default. Use 'pkey=True' to include that column's
        name as well.
        """
        sql = 'PRAGMA table_info(%s)' % (self.table)
        columns = self.curs.execute(sql).fetchall()
        names = []
        for i in range(len(columns)):
            if pkey == False and columns[i][0] == 0:
                continue
            names.append(columns[i][1])
        return names

    def get_column_types(self, pkey=False):
        """
        Return a list of the table's column data-types. The table's primary key
        is not included, by default. Use 'pkey=True' to include that column's
        type as well.
        """
        sql = 'PRAGMA table_info(%s)' % (self.table)
        columns = self.curs.execute(sql).fetchall()
        types = []
        for i in range(len(columns)):
            if pkey == False and columns[i][0] == 0:
                continue
            types.append(columns[i][2])
        return types

    def get_all_records(self):
        """
        Return a list of all table records.
        """
        sql = 'SELECT * FROM %s' % (self.table)
        print(sql)
        return self.curs.execute(sql).fetchall()

    def get_records(self, **kwargs):
        """
        Return a list of the database records that match the passed search
        criteria.
        """
        sql = 'SELECT * FROM %s WHERE' % (self.table)
        for key in kwargs:
            if not kwargs[key]:
                continue
            sql += ' %s="%s" AND' % (key, kwargs[key])
        sql = sql[:-4]
        print(sql)
        return self.curs.execute(sql).fetchall()

    def add_record(self, record):
        """
        Add a new database record.
        """
        sql = 'INSERT INTO %s VALUES (NULL' % (self.table)
        for field in record:
            sql += ', "%s"' % (field)
        sql += ')'
        print(sql)
        self.curs.execute(sql)
        self.conn.commit()

    def update_record(self, id, **kwargs):
        """
        Update change(s) into the database record that corresponds with the
        passed 'id'.
        """
        sql = 'UPDATE %s SET (' % (self.table)
        for key in kwargs:
            sql += '%s, ' % (key)
        sql = sql[:-2]
        sql += ') = ('
        for key in kwargs:
            sql += '"%s", ' % (kwargs[key])
        sql = sql[:-2]
        sql += ') WHERE id=%s' % (id)
        print(sql)
        self.curs.execute(sql)
        self.conn.commit()

    def delete_record(self, id):
        """
        Delete the database record that corresponds with the passed 'id'.
        """
        sql = 'DELETE FROM %s WHERE id=%s' % (self.table, id)
        print(sql)
        self.curs.execute(sql)
        self.conn.commit()

    def close(self):
        """
        Close the connection to the database.
        """
        self.conn.close()
