def get():
    info = {}
    info.update(
{ 'author': 'Polka',
  'author_email': 'ph.ebe.po.lk@gmail.com',
  'classifiers': [ 'Development Status :: 2 - Pre-Alpha',
                   'License :: OSI Approved :: BSD License',
                   'Programming Language :: Python',
                   'Intended Audience :: Developers'],
  'description': 'An interface with the 511 Real Time Departures api in the SF Bay area.',
  'long_description': "py511SFBay - Real Time Departures 511 SF Bay\n--------------------------------------\n\nAn interface with the 511 Real Time Departures api in the SF Bay area.\n\n\nInstallation\n------------\n\nUse::\n\n    > sudo pip install py511SFBay\n\nor::\n\n    > sudo easy install py511SFBay\n\nor::\n\n    > git clone git://github.com/polkapolka/py511SFBay.git\n    > cd py511SFBay\n    > sudo make install\n\nUsage\n-----\n\nFlee -l -a 'Caltrain' -rn 'BABY BULLET' -d 'NB'          # List the Stops on the Route\nFlee -m -sc 70141 70011                                  # Get the departures\nFlee -s                                                  # Setup a home and work csv\nFlee home                                                # call the home list\nFlee work                                                # call the work list\n\nConfiguration\n-----\n\nRTD_API_KEY - the RTD API key to use when fetching information. A public one is used by default, but you can get your own here.\nHOME_LIST - the location of a csv of stopcodes near your home\nWORK_LIST - the location of a csv of stopcodes near your work\n\nDevelopment Status\n------------------\n\nversion: 0.0.1\n\nCommunity\n---------\n\nAuthors\n-------\n\n* Polka <ph.ebe.po.lk@gmail.com>\n\nCopyright\n---------\n\npy511SFBay is Copyright (c) 2016, Polka\n\npy511SFBay is licensed under the New BSD License. See the LICENSE file.\n",
  'name': 'py511SFBay',
  'packages': ['py511SFBay'],
  'scripts': [],
  'url': 'http://github.com/polkapolka/py511SFBay/',
  'version': '0.0.1'}
)
    return info
