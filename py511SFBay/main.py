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

def get_args():
    #pdb.set_trace()
    parser = argparse.ArgumentParser(prog='flee',description="511 RTD API.  Use it to Flee your home or work. Why flee? Leave was already taken.",formatter_class=argparse.RawDescriptionHelpFormatter,
         epilog=textwrap.dedent('''Example uses:
           flee list -a 'Caltrain' -rn 'BABY BULLET' -d 'NB' \t\t# List the Stops on the Route
           flee stops 70141 70011 \t\t\t\t\t# Get the departures
           flee setup \t\t\t\t\t\t\t# Setup a home and work csv
           flee home \t\t\t\t\t\t\t# call the home list
           flee work \t\t\t\t\t\t\t# call the work list'''))
    subparsers = parser.add_subparsers(title="Commands", dest="command")
    p0 = subparsers.add_parser('list', help='List available options')
    p4 = subparsers.add_parser('stops', help='Returns the departure times at a list of station codes.')
    p1 = subparsers.add_parser('setup', help='Enter setup mode to make a home and a work list of station codes.')
    p2 = subparsers.add_parser('home', help='Display HOME_LIST')
    p3 = subparsers.add_parser('work', help='Display WORK_LIST')
    p0.add_argument('-a', nargs='?', help='511 transit agencies', dest='agency', choices=agencies.keys())
    p0.add_argument('-rn', nargs='?', help='Routes Name. For buses use just the code number and not the full title.', dest='routeName')
    p0.add_argument('-d', nargs='?', help='Direction', dest='direction')
    p1.add_argument('-a', nargs='?', help='511 transit agencies', dest='agency', choices=agencies.keys())
    p1.add_argument('-rn', nargs='?', help='Routes Name. For buses use just the code number and not the full title.', dest='routeName')
    p1.add_argument('-d', nargs='?', help='Direction', dest='direction')
    p4.add_argument('stops', metavar='N', type=str, nargs='+', help='Station Codes. Returns the departure times at a list of stations by code.')
    # parser.add_argument('-a', nargs='?', help='511 transit agencies', dest='agency', choices=agencies.keys())
    # parser.add_argument('-rn', nargs='?', help='Routes Name. For buses use just the code number and not the full title.', dest='routeName')
    # parser.add_argument('-d', nargs='?', help='Direction', dest='direction')
    # parser.add_argument('-sn', nargs='?', help='Station Name.  Requires the agency variable.  Returns the departure times at the station.', dest='stationName')
    #parser.add_argument('stops', metavar='N', type=str, nargs='+', help='Station Codes. Returns the departure times at a list of stations by code.')
    # group = parser.add_mutually_exclusive_group(required=True)
    # group.add_argument('-l', action='store_true', help='List Mode. List available options', default=False, dest='list')
    # group.add_argument('-m', action='store_true', help='Departure Mode. Return a departure time from stopcode or agency and stopname', default=False, dest='mode')
    # group.add_argument('-s', action='store_true', help='Setup Mode. Enter setup mode to make a home and a work list of station codes.', default=False, dest='setup')
    # #group.add_argument('home', help='Display HOME_LIST')
    return parser.parse_args()


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
    sList = ()
    with open(filename) as csvfile:
        reader=csv.reader(csvfile)
        for row in reader:
            departures=rtd.get_departures(stationCode=row)
            sList += ((departures['name'],departures['code']),)
    return sList

def make_csv(filename):
    with open(filename, 'wb') as csvfile:
        pass
    return


#logger.debug(rtd.get_stations('Caltrain','LIMITED','NB'))

def main():
    args = get_args()
    #pdb.set_trace()
    # -l enables list mode
    if args.command=='list':
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
    elif args.command == 'stops':
        #pdb.set_trace()
        if args.stops is not None:
            try:
                stations=[]
                for stationCode in args.stops:
                    departures = rtd.get_departures( stationCode=stationCode)
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
            #pprint(departures)
        # elif args.agency is not None and args.stationName is not None:
        #     try:
        #         departures = rtd.get_departures(args.agency, stationName=args.stationName)
        #         #wrapper(start_stuff)
        #         #draw_departures.start_stuff(departures)
        #     except RuntimeError as error:
        #         logger.critical(error)
        #     logger.debug(departures)
        #     pprint(departures)
        else:
            print "Station Code needed to return departure times.\n  Try the list command \'flee list\' to find the right Station Code."

    # -s enables setup mode
    # setup mode creates a list of home stations and a list of work stations
    # these can be called by simply using rtd home or rtd work
    # 
    elif args.command == 'setup':
        if os.path.isfile(settings.HOME_LIST) == False:
            print "Generating HOME_LIST."
            make_csv(settings.HOME_LIST)
        elif os.path.isfile(settings.WORK_LIST) == False:
            print "Generating WORK_LIST."
            make_csv(settings.WORK_LIST)
        try:
            draw_departures.start_setup(getStationNames(settings.HOME_LIST),getStationNames(settings.WORK_LIST))
        except RuntimeError as error:
        	logger.critical(error)

    elif args.command == 'home':
        try:
            os.path.isfile(settings.HOME_LIST)
        except IOError as error:
            logger.critical(error)
            print "HOME_LIST needed to run \'flee home\'.  Try the setup command \'flee setup\' to make a new HOME_LIST or change the filepath for the \'HOME_LIST\' value in settings.py."
        print "home command here"
    elif args.command == 'work':
        try:
            os.path.isfile(settings.WORK_LIST)
        except IOError as error:
            logger.critical(error)
            print "WORK_LIST needed to run \'flee work\'.  Try the setup command \'flee setup\' to make a new WORK_LIST or change the filepath for the \'WORK_LIST\' value in settings.py."
        print "work command here"


if __name__=='__main__':
    main()
