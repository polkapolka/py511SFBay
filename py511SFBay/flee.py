import argparse
import api
import logging
import settings
import sys
import os.path
import csv
import draw_departures
#from pprint import pprint
from datetime import datetime
#from draw_departures import start_stuff
from curses import wrapper
from parse_twitter import Station, Departure
import textwrap

import pdb

logging.basicConfig(filename="debug.log",level=logging.DEBUG)


logger = logging.getLogger()

rtd = api.RTD(settings.DEFAULT_API_KEY)
try:
    agencies = rtd.get_agencies()
except RuntimeError as error:
    logger.critical(error)

logger.debug(agencies)

parser = argparse.ArgumentParser(prog='flee',description="511 RTD API.  Use it to Flee your home or work. Why flee? Leave was already taken.",formatter_class=argparse.RawDescriptionHelpFormatter,
     epilog=textwrap.dedent('''Example uses:
       flee -l -a 'Caltrain' -rn 'BABY BULLET' -d 'NB' \t\t# List the Stops on the Route
       flee -m -sc 70141 70011 \t\t\t\t\t# Get the departures
       flee -s \t\t\t\t\t\t\t# Setup a home and work csv
       flee home \t\t\t\t\t\t# call the home list
       flee work \t\t\t\t\t\t# call the work list'''))

parser.add_argument('-a', nargs='?', help='511 transit agencies', dest='agency', choices=agencies.keys())
parser.add_argument('-rn', nargs='?', help='Routes Name. For buses use just the code number and not the full title.', dest='routeName')
parser.add_argument('-d', nargs='?', help='Direction', dest='direction')
parser.add_argument('-sn', nargs='?', help='Station Name.  Requires the agency variable.  Returns the departure times at the station.', dest='stationName')
parser.add_argument('-sc', nargs='+', help='Station Codes. Returns the departure times at a list of stations by code.', dest='stationCodes')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-l', action='store_true', help='List Mode. List available options', default=False, dest='list')
group.add_argument('-m', action='store_true', help='Departure Mode. Return a departure time from stopcode or agency and stopname', default=False, dest='mode')
group.add_argument('-s', action='store_true', help='Setup Mode. Enter setup mode to make a home and a work list of station codes.', default=False, dest='setup')
#group.add_argument('home', help='Display HOME_LIST')
args = parser.parse_args()


def addDeparturesToStation(newStation, departures):
    #pdb.set_trace()
    for route, directions in departures.items():
        for direction, times in directions.items():
            for time in times:
                #pdb.set_trace()
                d = Departure(route, direction, time)
                newStation.add_departure(d)


def getStationNames(filename):
    #pdb.set_trace()
    sList = []
    with open(filename) as csvfile:
        reader=csv.reader(csvfile)
        for row in reader:
            departures=rtd.get_departures(stationCode=row)
            sList.append((departures['name'],departures['code']))
    return sList


#logger.debug(rtd.get_stations('Caltrain','LIMITED','NB'))

# -l enables list mode
if args.list:
    if args.direction is not None and args.routeName is not None:
        if args.agency == "BART":
            #pdb.set_trace()
            routes = rtd.get_routes(args.agency)
            stops = rtd.get_stations(args.agency, routes[args.routeName]["Code"])
        else:
            try:
                stops = rtd.get_stations(args.agency, args.routeName, args.direction)
            except RuntimeError as error:
                logger.critical(error)
            logger.debug(stops)
        print "Code".ljust(14), " - ", "Stop Name"
        for stop in sorted(stops.keys()):
            sys.stdout.flush()
            print stops[stop].ljust(14)," - ",stop
    elif args.agency is not None:
        try:
            routes = rtd.get_routes(args.agency)
        except RuntimeError as error:
            logger.critical(error)
        logger.debug(routes)
        if agencies[args.agency]:
            print "Route".ljust(30)," - ", "Directions"
            for route in routes.keys():
                sys.stdout.flush()
                if args.agency != "BART":
                    print route.ljust(30)," - ",routes[route]['Direction'].values()
                elif args.agency == "BART":
                    '''BART only has Routes with no direction.  The route is the direction.'''
                    print route.ljust(30), " - ", route
    else:
        #pdb.set_trace()
        print "Agency - Type"
        for agency, mode in agencies.items():
            print "%s - %s" % (agency, mode)
        #pdb.set_trace()

# need a function to get station name from station code and vice versa
# -m enables departure mode
elif args.mode:
    #pdb.set_trace()
    if args.stationCodes is not None:
        try:
            stations=[]
            for stationCode in args.stationCodes:
                departures = rtd.get_departures(args.agency, stationCode=stationCode)
                newStation = Station(agency=departures['agency'], code=departures['code'], name=departures['name'])
                addDeparturesToStation(newStation, departures['routes'])
                #wrapper(start_stuff)
                newStation.order_departures()
                stations.append(newStation)
                #pdb.set_trace()
            draw_departures.start_other_stuff(stations)
        except RuntimeError as error:
            logger.critical(error)
        logger.debug(departures)
        pprint(departures)
    elif args.agency is not None and args.stationName is not None:
        try:
            departures = rtd.get_departures(args.agency, stationName=args.stationName)
            #wrapper(start_stuff)
            #draw_departures.start_stuff(departures)
        except RuntimeError as error:
            logger.critical(error)
        logger.debug(departures)
        pprint(departures)
    else:
        print "Station Name or Station Code needed to return departure times.\n  Try list mode \'-l\' to find the right Station info."

# -s enables setup mode
# setup mode creates a list of home stations and a list of work stations
# these can be called by simply using rtd home or rtd work
# 
elif args.setup:
    try:
        os.path.isfile(settings.HOME_LIST)
    except IOError as error:
        logger.critical(error)
    try:
        os.path.isfile(settings.WORK_LIST)
    except IOError as error:
        logger.critical(error)
    try:
        draw_departures.start_setup(getStationNames(settings.HOME_LIST),getStationNames(settings.WORK_LIST))
    except RuntimeError as error:
    	logger.critical(error)


