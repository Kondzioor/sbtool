r"""
Server Api module
"""
from SimpleXMLRPCServer import SimpleXMLRPCServer

from sbtool.server.gateways import Database
from sbtool.server.stuff import Stuff


class Api(object):
    """ Server Api, controls access to booking stuff"""

    def __init__(self, stuffs):
        self.stuffs = stuffs

    def list_stuff(self):
        """ Returns all stuffs with current status """
        output = {}
        for stuff in self.stuffs:
            helper = {stuff.name: stuff.status()}
            if stuff.type in output:
                output[stuff.type].update(helper)
            else:
                output[stuff.type] = helper
        return output

    def status(self, name):
        """ Returns stuff status with given name"""
        stuffs = [stuff for stuff in self.stuffs if stuff.name in name]
        if stuffs:
            return stuffs[0].status()
        return Stuff.NOK

    def reserve_stuff(self, name, user):
        """ Reserves stuff with given name for given user """
        free_stuff = [stuff for stuff in self.stuffs
                      if stuff.name == name
                      and stuff.status() == Stuff.OK]
        if free_stuff:
            return free_stuff[0].reserve(user)
        return False

    def reserve(self, stuff_type, user):
        """ Reserve first available stuff for given type"""
        stuffs = [stuff for stuff in self.stuffs
                  if stuff.type == stuff_type and stuff.status() == Stuff.OK]
        if stuffs and stuffs[0].reserve(user):
            return stuffs[0].name
        return False

    def release(self, name):
        """ Releases stuff with given name"""
        stuff = [stuff for stuff in self.stuffs if stuff.name == name
                 and stuff.status() != Stuff.OK
                 and stuff.status() != Stuff.NOK]

        if stuff:
            return stuff[0].release()
        return False


def run(conf):
    """ Runs Server with given configuration """
    dbase = Database(conf.SERVER['db_name'])
    stuffs = []
    for stuff_type, stuff_names in conf.STUFF_TO_BOOKING.iteritems():
        stuffs.extend([Stuff(stuff_type, name, dbase) for name in stuff_names])
    api = Api(stuffs)
    server = SimpleXMLRPCServer((conf.SERVER['host'], conf.SERVER['port']),
                                allow_none=True)
    server.register_instance(api)
    server.serve_forever()
