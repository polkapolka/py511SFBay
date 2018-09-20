py511SFBay - Real Time Departures 511 SF Bay
--------------------------------------

An interface with the 511 Real Time Departures api in the SF Bay area.


Installation
------------

Use::

    > sudo pip install py511SFBay

or::

    > sudo easy install py511SFBay

or::

    > git clone git://github.com/polkapolka/py511SFBay.git
    > cd py511SFBay
    > sudo make install

Usage
-----

Flee list -a 'Caltrain' -rn 'BABY BULLET' -d 'NB'        # List the Stops on the Route
Flee stops 70141 70011                                   # Get the departures
Flee setup                                               # Setup a home and work csv
Flee home                                                # call the home list
Flee work                                                # call the work list

Configuration
-----

RTD_API_KEY - the RTD API key to use when fetching information. A public one is used by default, but you can get your own here.
HOME_LIST - the location of a csv of stopcodes near your home
WORK_LIST - the location of a csv of stopcodes near your work

Development Status
------------------

version: 0.0.1

Community
---------

Authors
-------

* Polka <ph.ebe.po.lk@gmail.com>

Copyright
---------

py511SFBay is Copyright (c) 2016, Polka

py511SFBay is licensed under the New BSD License. See the LICENSE file.
