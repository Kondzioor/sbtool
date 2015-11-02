r"""
Stuff wrapper
"""
from sbtool.server.gateways import Reservation


class Stuff(object):
    """ Stuff wrapper """

    NOK = 'not available'

    def __init__(self, stype, name, gateway):
        self._type = stype
        self._name = name
        self.gateway = gateway

    @property
    def name(self):
        """ Stuff name"""
        return self._name

    @property
    def type(self):
        """ Stuff type"""
        return self._type

    def status(self):
        """ Returns stuff status """
        result = self.gateway.get_active_reservations(self.type, self.name)
        if result:
            return result[0]
        return Reservation(self.type, self.name)

    def reserve(self, user):
        """ Reserves stuff for given user, returns true if success """
        return self.gateway.reserve(self.type, self.name, user)

    def release(self):
        """ Releases stuff, returns true if success """
        return self.gateway.release(self.type, self.name)
