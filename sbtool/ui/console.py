#!/usr/bin/env python
r"""
Console client for sbtool
"""
import socket
import xmlrpclib
import getpass

import argparse


class Application(object):
    """ Command line client """

    def __init__(self, parser, options):
        self._conn = Application.connect(options.host, options.port)
        self.act(parser, options)

    def act(self, parser, options):
        """ Dispatches user chose"""
        if options.list:
            self.display_list()
        elif options.reserve:
            self.reserve(options.reserve)
        elif options.release:
            self.release(options.release)
        elif options.status:
            self.status(options.status)
        else:
            parser.print_help()

    @staticmethod
    def connect(server, port):
        """ Connects to server and returns connection object"""
        return xmlrpclib.ServerProxy('http://{0}:{1}'.format(server, port),
                                     allow_none=True)

    def display_list(self):
        """ Displays stuff list"""
        for name, stat in self._conn.list_stuff().iteritems():
            print("{0}: {1}".format(name, stat))

    def reserve(self, name):
        """ Reserves stuff """
        user = getpass.getuser()
        Application.print_result(self._conn.reserve(name, user))

    def release(self, name):
        """ Releases stuff """
        Application.print_result(self._conn.release(name))


    @staticmethod
    def print_result(result):
        """ Prints operation result"""
        if result:
            print('Success')
        else:
            print("Failed")

    def status(self, name):
        """ Shows stuff status"""
        print(self._conn.status(name.strip()))


def run(config):
    """Runs command line client"""
    address = config.UI['server_host']
    port = config.UI['server_port']

    parser = argparse.ArgumentParser(description="Runs e2e test for SMC.")
    parser.add_argument('--list', action='store_true', help='list all stuff')
    parser.add_argument('--reserve', help='reserve stuff from selected type')
    parser.add_argument('--release', help='release stuff')
    parser.add_argument('--status', help='returns stuff status')
    parser.add_argument('--host',
                        help='override default {0} host'.format(address))
    parser.add_argument('--port',
                        help='override default {0} port'.format(port))
    parser.set_defaults(list=None, host=address, port=port)
    options = parser.parse_args()
    try:
        Application(parser, options)
    except socket.error as err:
        print(err)
