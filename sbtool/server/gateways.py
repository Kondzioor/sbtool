r"""
Module responsible for gateway with database
"""
import sqlite3
import datetime


class Reservation(object):
    """ Database reservation row wrapper"""
    def __init__(self, row):
        self._name = row[Database.NAME]
        self._user_name = row[Database.USER_NAME]
        self._reservation_start = row[Database.RESERVATION_START]

    @property
    def name(self):
        """ Stuff name """
        return self._name

    @property
    def user_name(self):
        """ Reservation for user name """
        return self._user_name

    @property
    def reservation_start(self):
        """ Reservation start date """
        return self._reservation_start


class Database(object):
    """ Database gateway"""

    NAME = 0
    USER_NAME = 1
    RESERVATION_START = 2

    def __init__(self, db_name):
        self._conn = sqlite3.connect(db_name)
        with self._conn:
            self._conn.execute(
                '''CREATE TABLE IF NOT EXISTS reservation
                   (name TEXT,
                    user_name TEXT,
                    reservation_start INTEGER,
                    reservation_end INTEGER)''')

    def get_active_reservations(self, name=None):
        """ Returns all active reservations """
        with self._conn:
            return [
                Reservation(row)
                for row in self._get_active_reservations(name)
            ]

    def reserve(self, name, user_name):
        """ Reserve stuff with given name for user return true if success s"""
        with self._conn:
            row = self._get_active_reservations(name)
            if not row:
                self._conn.execute('''INSERT INTO reservation
                                VALUES(?, ?, ?, ?)''',
                                   (name, user_name,
                                    datetime.datetime.now(), None))
                return True
        return False

    def release(self, name):
        """ Releases reservation for given name, return true if success"""
        with self._conn:
            row = self._get_active_reservations(name)
            if row:
                self._conn.execute(
                    '''UPDATE reservation SET
                         reservation_end = ?
                       where reservation_end is null and name = ?''',
                    (datetime.datetime.now(), name, ))
                return True
            return False

    def _get_active_reservations(self, name=None):
        """ Gets all active reservation with given name """
        cmd = 'SELECT * FROM reservation WHERE reservation_end IS NULL'
        cmd = Database._append_command_to_sql_command(cmd, 'name', name)
        result = self._conn.execute(cmd)
        return result.fetchmany()

    @staticmethod
    def _append_command_to_sql_command(cmd, name, value):
        """Appends where statement to sql command """
        if value:
            return ' '.join([cmd, 'and', name, '=', '\"{0}\"'.format(value)])
        return cmd
