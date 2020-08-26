import os
import argparse
import hashlib
import sqlite3


def main():

    my_name = __file__
    my_path = os.path.dirname(__file__)

    p = argparse.ArgumentParser(
        description='This is a script to get file info from a given file tree. ')
    p.add_argument('dir', type=str, help='path to starting directory')
    p.add_argument('db', type=str, help='path to sqlite3 database')
    # p.add_argument('checksum', type=bool, help='include checksum?')
    p.add_argument('--checksum', default=False,
                   action='store_true', help='include checksum?')
    args = p.parse_args()

    if os.path.isdir(args.dir):
        root_dir = args.dir
    else:
        print('Error: ' + args.dir + ' is not a directory!')
        exit

    if os.path.isfile(args.db):
        db_path = args.db
    else:
        print('Error: ' + args.db + ' not found!')
        exit

    # Connect to database and insert rows
    with sqlite3.connect(db_path) as db:

        for root, dirs, files in os.walk(root_dir, followlinks=False):
            for name in files:
                my_path = os.path.join(root, name)
                # Obtain file information
                file_info = get_file_info(my_path, checksum=args.checksum)
                # insert as row in db
                print("Inserting: " + file_info[0])
                x = sq_insert_row(db, file_info)
                # print(x)


def get_file_info(_path, checksum=False):
    _name = os.path.basename(_path)
    _size = os.path.getsize(_path)
    _dir = os.path.dirname(_path)
    _date = os.path.getmtime(_path)
    if checksum:
        _checksum = hashlib.md5(open(_path, 'rb').read()).hexdigest()
    else:
        _checksum = None
    return (_path, _name, _dir, _size, _date, _checksum)


def sq_insert_row(conn, row):
    try:
        sqliteConnection = conn
        cursor = sqliteConnection.cursor()
        # print("Successfully Connected to SQLite")

        sqlite_insert_query = """INSERT INTO files
                            (path,name,dir,size,updated,checksum)
                            VALUES 
                            (?,?,?,?,?,?)"""

        count = cursor.execute(sqlite_insert_query, row)
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data: " + str(row), error)
    # finally:
    #     if (sqliteConnection):
    #         sqliteConnection.close()
    #         print("The SQLite connection is closed")


if __name__ == "__main__":
    main()
