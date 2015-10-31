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
        return dict((stuff.name, stuff.status())
                    for stuff in self.stuffs)

    def status(self, name):
        """ Returns stuff status with given name"""
        stuffs = [stuff for stuff in self.stuffs if stuff.name in name]
        if stuffs:
            return stuffs[0].status()
        return Stuff.NOK

    def reserve(self, name, user):
        """ Reserves stuff with given name for given user """
        free_stuff = [stuff for stuff in self.stuffs
                      if stuff.name == name
                      and stuff.status() == Stuff.OK]
        if free_stuff:
            return free_stuff[0].reserve(user)
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
    stuffs = [Stuff(stuff, dbase) for stuff in conf.STUFF_TO_BOOKING]
    api = Api(stuffs)
    server = SimpleXMLRPCServer((conf.SERVER['host'], conf.SERVER['port']),
                                allow_none=True)
    server.register_instance(api)
    server.serve_forever()
