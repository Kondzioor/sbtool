import unittest

from sbtool.server.gateways import Database


DB_NAME = ":memory:"
USER_NAME = "user_name"
NAME = 'name'
TYPE = 'type'


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.uut = Database(DB_NAME)

    def assertReservation(self, reservation):
        self.assertEquals(USER_NAME, reservation.user_name)
        self.assertIsNotNone(reservation.reservation_start)
        self.assertEquals(TYPE, reservation.type)
        self.assertEquals(NAME, reservation.name)

    def test_when_empty_db_then_return_empty_list(self):
        self.assertFalse(self.uut.get_active_reservations())

    def test_when_name_not_reserved_then_return_empty_list(self):
        self.assertFalse(self.uut.get_active_reservations())
        self.assertFalse(self.uut.get_active_reservations(stuff_name=NAME))
        self.assertFalse(self.uut.get_active_reservations(stuff_type=TYPE))
        self.assertFalse(self.uut.get_active_reservations(stuff_type=TYPE,
                                                          stuff_name=NAME))

    def test_when_reservation_success_then_return_reserved_list(self):
        self.assertTrue(self.uut.reserve(stuff_type=TYPE,
                                         stuff_name=NAME,
                                         user_name=USER_NAME))

        result = self.uut.get_active_reservations()
        self.assertEquals(1, len(result))
        self.assertReservation(result[0])

    def test_when_stuff_already_reserved_then_return_false(self):
        self.assertTrue(self.uut.reserve(stuff_type=TYPE,
                                         stuff_name=NAME,
                                         user_name=USER_NAME))

        self.assertFalse(self.uut.reserve(stuff_type=TYPE,
                                          stuff_name=NAME,
                                          user_name=USER_NAME))

    def test_when_release_failed_then_return_false(self):
        self.assertFalse(self.uut.release(stuff_type=TYPE, stuff_name=NAME))

    def test_should_release_reservation(self):
        self.uut.reserve(stuff_type=TYPE, stuff_name=NAME, user_name=USER_NAME)

        self.assertTrue(self.uut.release(stuff_type=TYPE, stuff_name=NAME))
        self.assertFalse(self.uut.get_active_reservations())
