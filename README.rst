BTS Reservation Tool
====================

Overview
--------

	Tool designed for simple staff booking.

Components
----------

**Server**

	Responsible for booking all stuff when is user sends requests.

**Console UI**

	Responsible for interaction with user by CLI. Running on user machine.



Usage
-----

First step is to create your config file. As a example you can use config_default.py.

Then distribute software on PC which you want to use.

On server node with --server swich
On web server node with --web

And that is all :)


Testing
-------

To run all test call run_test.py script


Troubleshooting
---------------
When you don't have flask to run web client, and you don't have root right to install it or
packages are not available for some reason in your distribution then you must use virtualenv configuration.

First install virtualenv utility
sudo apt-get install python-virtualenv #in Debian/Ubuntu

-Create virtual env
cd web_client
virtualenv env

-Install Dependencies
env/bin/pip install -r requirements

-Then run :)
./run.py --web

