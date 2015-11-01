r"""
Stuff wrapper
"""


class Stuff(object):
    """ Stuff wrapper """

    OK = 'available'
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
            return "since {0}, user {1}".format(
                result[0].reservation_start, result[0].user_name)
        return Stuff.OK

    def reserve(self, user):
        """ Reserves stuff for given user, returns true if success """
        return self.gateway.reserve(self.type, self.name, user)

    def release(self):
        """ Releases stuff, returns true if success """
        return self.gateway.release(self.type, self.name)
