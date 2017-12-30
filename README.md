# db-app
A simple user interface to administer an Sqlite database.

    Usage: db-app.py [--seed] [--title TITLE] [--path DIRECTORY] DB_NAME
           db-app.py --help

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
        
Thank you to Ardit Sulce, Instructor of [The Python Mega Course](https://www.udemy.com/the-python-mega-course/learn/v4/overview "Udemy.com"), for introducing
a simplified version of this app in sections 16 and 17 of the course material.
