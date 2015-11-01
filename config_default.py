r"""
It's default configuration file.
"""

STUFF_TO_BOOKING = {
    'type_1': ['type_1_stuff_1',
               'type_1_stuff_2',
               'type_1_stuff_3'],
    'type_2': ['type_2_stuff_1',
               'type_2_stuff_2',
               'type_3_stuff_3']
}

SERVER = {
    'db_name': 'booking_history.db',
    'host': '0.0.0.0',
    'port': 8000
}

UI = {
    'server_host': 'localhost',
    'server_port': SERVER['port']
}

CONSOLE = UI.copy()
WEB = UI.copy()

WEB['host'] = '0.0.0.0'
WEB['port'] = 5000
