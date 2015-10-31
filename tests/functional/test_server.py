import unittest

from sbtool.server.stuff import Stuff
from sbtool.server.gateways import Database
from sbtool.server.api import Api


USER = "user"
TYPE = "type_1"
STUFF_1 = 'stuff_1'
STUFF_2 = 'stuff_2'
STUFF_3 = 'stuff_3'
STUFFS = [STUFF_1, STUFF_2]


class TestApi(unittest.TestCase):

    def setUp(self):
        db = Database(":memory:")
        stuffs = [Stuff(stuff, db) for stuff in STUFFS]

        self.uut = Api(stuffs)

    def test_when_list_stuff_called_then_all_stuff_returned(self):
        result = self.uut.list_stuff()

        self.assertEquals(len(STUFFS), len(result))
        self.assertEquals(Stuff.OK, result[STUFF_1])
        self.assertEquals(Stuff.OK, result[STUFF_2])

    def test_when_status_called_and_stuff_exists_then_return_status_ok(self):
        self.assertEquals(Stuff.OK, self.uut.status(STUFF_1))

    def test_when_status_called_and_stuff_not_exists_then_return_nok(self):
        self.assertEquals(Stuff.NOK, self.uut.status(STUFF_3))

    def test_when_stuff_reserved_then_return_status_nok(self):
        self.assertTrue(self.uut.reserve(STUFF_1, USER))
        self.assertIn('user user', self.uut.status(STUFF_1))

    def test_should_return_false_when_reserve_called_more_than_once(self):
        self.assertTrue(self.uut.reserve(STUFF_1, USER))
        self.assertFalse(self.uut.reserve(STUFF_1, USER))

    def test_when_stuff_not_exist_then_reserve_return_false(self):
        self.assertFalse(self.uut.reserve(STUFF_3, USER))

    def test_should_release_stuff_when_reserved(self):
        self.uut.reserve(STUFF_1, USER)
        self.assertTrue(self.uut.release(STUFF_1))

    def test_when_reservation_not_exist_then_return_false(self):
        self.assertFalse(self.uut.release(STUFF_1))

    def test_when_staff_reserved_then_list_should_be_updated(self):
        self.uut.reserve(STUFF_1, USER)

        result = self.uut.list_stuff()
        self.assertEquals(len(STUFFS), len(result))
        self.assertNotEquals(Stuff.OK, result[STUFF_1])
        self.assertNotEquals(Stuff.NOK, result[STUFF_1])
        self.assertEquals(Stuff.OK, result[STUFF_2])
