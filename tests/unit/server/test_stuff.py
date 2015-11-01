import unittest
import mock

from sbtool.server.stuff import Stuff

NAME = 'name'
TYPE = 'type'
USER = 'user'


class TestSlave(unittest.TestCase):

    def setUp(self):
        self.gateway_mock = mock.Mock()
        self.uut = Stuff(TYPE, NAME, self.gateway_mock)

    def test_when_called_release_then_invoke_release(self):
        self.uut.release()
        self.gateway_mock.release.assert_called_once(TYPE, NAME)

    def test_when_reserve_called_then_invoke_reserved(self):
        self.uut.reserve(USER)
        self.gateway_mock.reserve.assert_called_once_with(TYPE, NAME, USER)

    def test_when_status_called_then_invoke_status(self):
        self.gateway_mock.get_active_reservations.return_value = []
        self.assertEquals(Stuff.OK, self.uut.status())
