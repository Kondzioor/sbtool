import unittest

from sbtool.server.stuff import Stuff
from sbtool.server.gateways import Database
from sbtool.server.api import Api


USER = "user"
TYPE = "type_1"
STUFF_1 = 'stuff_1'
STUFF_2 = 'stuff_2'
STUFF_3 = 'stuff_3'
TYPE_1 = 'type_1'
TYPE_2 = 'type_2'
TYPE_3 = 'type_3'
STUFFS = {TYPE_1: [STUFF_1],
          TYPE_2: [STUFF_2]}


class TestApi(unittest.TestCase):

    def setUp(self):
        db = Database(":memory:")
        stuffs = []
        for stuff_type, stuff_names in STUFFS.iteritems():
            stuffs.extend([Stuff(stuff_type, name, db)
                           for name in stuff_names])

        self.uut = Api(stuffs)

    def assertIsAvailable(self, result):
        self.assertIsNone(result.user_name)
        self.assertIsNone(result.reservation_start)

    def assertIsReserved(self, name, result):
        self.assertEqual(name, result.user_name)
        self.assertIsNotNone(result.reservation_start)

    def test_when_list_stuff_called_then_all_stuff_returned(self):
        result = self.uut.list_stuff()

        self.assertEquals(len(STUFFS), len(result))
        self.assertIsAvailable(result[TYPE_1][STUFF_1])
        self.assertIsAvailable(result[TYPE_2][STUFF_2])

    def test_when_status_called_and_stuff_exists_then_return_status_ok(self):
        self.assertIsAvailable(self.uut.status(STUFF_1))

    def test_when_status_called_and_stuff_not_exists_then_return_nok(self):
        self.assertEquals(Stuff.NOK, self.uut.status(STUFF_3))

    def test_when_stuff_reserved_then_return_status_nok(self):
        self.assertTrue(self.uut.reserve_stuff(STUFF_1, USER))

        result = self.uut.status(STUFF_1)
        self.assertEqual(result.type, TYPE_1)
        self.assertEqual(result.name, STUFF_1)
        self.assertEqual(result.user_name, USER)
        self.assertIsNotNone(result.reservation_start)

    def test_should_return_false_when_reserve_called_more_than_once(self):
        self.assertTrue(self.uut.reserve_stuff(STUFF_1, USER))
        self.assertFalse(self.uut.reserve_stuff(STUFF_1, USER))

    def test_when_stuff_not_exist_then_reserve_return_false(self):
        self.assertFalse(self.uut.reserve_stuff(STUFF_3, USER))

    def test_should_release_stuff_when_reserved(self):
        self.uut.reserve_stuff(STUFF_1, USER)
        self.assertTrue(self.uut.release(STUFF_1))

    def test_when_reservation_not_exist_then_return_false(self):
        self.assertFalse(self.uut.release(STUFF_1))

    def test_when_staff_reserved_then_list_should_be_updated(self):
        self.uut.reserve_stuff(STUFF_1, USER)

        result = self.uut.list_stuff()
        self.assertEquals(len(STUFFS), len(result))
        self.assertIsReserved(USER, result[TYPE_1][STUFF_1])
        self.assertIsAvailable(result[TYPE_2][STUFF_2])

    def test_when_no_available_stuff_with_given_type_then_return_false(self):
        self.assertFalse(self.uut.reserve(TYPE_3, USER))

    def test_should_return_stuff_name_when_is_available(self):
        self.assertEquals(STUFF_1, self.uut.reserve(TYPE_1, USER))
        self.assertFalse(self.uut.reserve(TYPE_1, USER))
