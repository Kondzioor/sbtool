r"""
Module responsible for gateway with database
"""
import sqlite3
import datetime


class Reservation(object):
    """ Database reservation row wrapper"""

    def __init__(self, stuff_type, stuff_name):
        self.type = stuff_type
        self.name = stuff_name
        self.user_name = None
        self.reservation_start = None

    @staticmethod
    def convert(row):
        reservation = Reservation(row[Database.TYPE], row[Database.NAME])
        reservation.user_name = row[Database.USER_NAME]
        reservation.reservation_start = row[Database.RESERVATION_START_TIME]
        return reservation


class Database(object):
    """ Database gateway"""

    TYPE = 0
    NAME = 1
    USER_NAME = 2
    RESERVATION_START_TIME = 3

    def __init__(self, db_name):
        self._conn = sqlite3.connect(db_name)
        with self._conn:
            self._conn.execute(
                '''CREATE TABLE IF NOT EXISTS reservation
                   (type TEXT,
                    name TEXT,
                    user_name TEXT,
                    reservation_start INTEGER,
                    reservation_end INTEGER)''')

    def get_active_reservations(self, stuff_type=None, stuff_name=None):
        """ Returns all active reservations """
        with self._conn:
            return [
                Reservation.convert(row)
                for row in self._get_active_reservations(stuff_type,
                                                         stuff_name)
            ]

    def reserve(self, stuff_type, stuff_name, user_name):
        """ Reserve stuff with given name for user return true if success s"""
        with self._conn:
            row = self._get_active_reservations(stuff_type, stuff_name)
            if not row:
                self._conn.execute('''INSERT INTO reservation
                                VALUES(?, ?, ?, ?, ?)''',
                                   (stuff_type, stuff_name, user_name,
                                    datetime.datetime.now(), None))
                return True
        return False

    def release(self, stuff_type, stuff_name):
        """ Releases reservation for given name, return true if success"""
        with self._conn:
            row = self._get_active_reservations(stuff_type, stuff_name)
            if row:
                self._conn.execute(
                    '''UPDATE reservation SET
                         reservation_end = ?
                       where reservation_end is null and name = ?
                        and type = ?''',
                    (datetime.datetime.now(), stuff_name, stuff_type, ))
                return True
            return False

    def _get_active_reservations(self, stuff_type=None, stuff_name=None):
        """ Gets all active reservation with given name """
        cmd = 'SELECT * FROM reservation WHERE reservation_end IS NULL'
        cmd = Database._append_command_to_sql_command(cmd, 'type', stuff_type)
        cmd = Database._append_command_to_sql_command(cmd, 'name', stuff_name)

        result = self._conn.execute(cmd)
        return result.fetchmany()

    @staticmethod
    def _append_command_to_sql_command(cmd, name, value):
        """Appends where statement to sql command """
        if value:
            return ' '.join([cmd, 'and', name, '=', '\"{0}\"'.format(value)])
        return cmd
