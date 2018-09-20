from datetime import datetime
from utils import Window
import settings
import pdb
import os
import curses
from pymsgbox import prompt

def start_setup(homelist, worklist):
    # Initialize window
    window = Window(settings.REFRESH_INTERVAL, settings.TOTAL_COLUMNS)
    def draw(homelist,worklist):
        def loop_until(window, stop):
            sc=''
            while True:
                if window.getch()==stop:
                    break
                sc.join(window.getch())
            return sc
        #pdb.set_trace()
        y=0
        x=int(round(.5*window.spacing))
        window.center(y,'Setup RTD Home and Work')
        y+=2
        window.addstr(y, x, "Home Stations", bold=True)
        x+=2*window.spacing
        window.addstr(y, x, "Work Stations", bold=True)
        y+=2
        for index in range(0,max([len(homelist),len(worklist)])):
            x=0
            if index <len(homelist):
                window.addstr(y, x,homelist[index][0])
            x+=window.spacing
            if index <len(homelist):
                window.addstr(y,x,homelist[index][1])
            x+= window.spacing
            if index <len(worklist):
                window.addstr(y,x,worklist[index][0])
            x+= window.spacing
            if index <len(worklist):
                window.addstr(y,x,worklist[index][1])
            y+=1
        y+=1
        x=0

        # Display help text at the bottom
        window.clear_lines(y + 1)
        x = 0
        window.addstr(y + 2, x, 'Press \'q\' to quit. Press \'a\' to Add station. Press \'r\' to Remove station.')

        # Clear the bottom 2 lines in case rows were moved up
        window.clear_lines(y + 3, lines=2)
        window.addstr(y, x, "Command: "+window.getch())
        # if window.getch()=='a':
        #     window.clear_lines(0,lines=y+3)
        #     y=0
        #     window.addstr(y,x,"Command: Add Station Code: ")
        #     x+=len("Command: Add Station Code: ")
        #     sc = prompt(text='', title='')
        #     window.addstr(y,0, "Add "+sc+" to home or work? Press \'h\' for home and \'w\'for work.")
        #     nchar=window.getch()
        #     while True:
        #         if nchar == 'h':
        #             #pdb.set_trace()
        #             fd = open('document.csv','a')
        #             fd.write(myCsvRow)
        #             fd.close()
        #             window.disable_echo()
        #             break
        #         elif nchar == 'w':
        #             worklist += (("New Station",sc),)
        #             window.disable_echo()
        #             break
        #         else:
        #             nchar= window.getch()
        # if window.getch()=='r':
        #     window.clear_lines(0,lines=y+3)
        #     y=0
        #     window.addstr(y,x,"Command: Remove Station Code: ")
        #     x+=len("Command: Remove Station Code: ")

    #function
    char = ''
    while True:
        try:
            draw(homelist, worklist)
        except RuntimeWarning:
            pass
        except RuntimeError as error:
            window.endwin()
            print(error)
            exit(1)

        char = window.getch()
        if char == "q" |char == "a"|char=="r":
            break
    window.endwin()


def start_other_stuff(stations):
    # Initialize window
    window = Window(settings.REFRESH_INTERVAL, settings.TOTAL_COLUMNS)
    def draw(stations):
        def get_minutes_color(minutes):
            """Get the color to use for the minutes estimate."""
            try:
                minutes = int(minutes.split()[0])
                if minutes <= 5:
                    return 'RED'
                elif minutes <= 10:
                    return 'YELLOW'
            except ValueError:
                return 'RED'
        y = 0
        # Display the current time
        # pdb.set_trace()
        window.center(y, 'RTD departures as of {time}'.format(
            time=datetime.now().strftime('%I:%M:%S %p')))
        stations = sorted(stations, key=lambda station: station.agency)
        cagency=""
        for station in stations:
            if station.agency != cagency:
                y+=2
                window.center(y, station.agency)
                cagency = station.agency
                y+=1
            x = window.spacing
            window.addstr(y,0,station.name,bold=True)
            y+=1
            for direction in station.get_directions():
                #y+=1
                window.addstr(y,0, direction.title())
                dep_list = station.get_departures_from_direction(direction)
                ts=x
                for i, departure in enumerate(dep_list):
                    window.addstr(y, x, '# ', color_name='ORANGE')
                    x+=2
                    color = get_minutes_color(str(departure.time))
                    #pdb.set_trace()
                    window.addstr(y,x, str(departure.time)+" min ", color_name=color)
                    x+=len(str(departure.time)+" min ")
                    window.addstr(y, x, "("+departure.route+")", color_name='GREEN')
                    x+=len("("+departure.route+")")
                    x = (i%3+2) * ts
                    if i%3==2 and i+1 < len(dep_list):
                        #pdb.set_trace()
                        y+=1
                        x=ts
                y+=1
                x=ts

        # Display help text at the bottom
        window.clear_lines(y + 1)
        x = 0
        window.addstr(y + 2, x, 'Press \'q\' to quit.')

        # Clear the bottom 2 lines in case rows were moved up
        window.clear_lines(y + 3, lines=2)

    #function
    char = ''
    while char!='q':
        try:
            draw(stations)
        except RuntimeWarning:
            pass
        except RuntimeError as error:
            window.endwin()
            print(error)
            exit(1)

        char = window.getch()
    window.endwin()



def start_stuff(departures):
    # Initialize window
    window = Window(settings.REFRESH_INTERVAL, settings.TOTAL_COLUMNS)
    def draw(things):
        def get_minutes_color(minutes):
            """Get the color to use for the minutes estimate."""
            try:
                minutes = int(minutes.split()[0])
                if minutes <= 5:
                    return 'RED'
                elif minutes <= 10:
                    return 'YELLOW'
            except ValueError:
                return 'RED'
        y = 0
        # Display the current time
        #pdb.set_trace()
        window.center(y, 'RTD departures as of {time}'.format(
            time=datetime.now().strftime('%I:%M:%S %p')))
        for thing in things:
            #y+=2
            x = window.spacing
            #window.addstr(y,0,thing)
            pdb.set_trace()
            for item in things[thing]:
                y+=2
                window.addstr(y,0, item)
                ts=x
                for i, dtime in enumerate(things[thing][item]):
                    window.addstr(y, x, '# ', color_name='ORANGE')
                    x+=2
                    color = get_minutes_color(dtime)
                    x+=ts
                    window.addstr(y,x, dtime + " min ", color_name=color)
                    x+=len(dtime + " min ")
                    #window.addstr(y,x, "("+thing['Route']+")", color_name='GREEN')
                    #x+=len("("+thing['Route']+")")
                y+=1

        # Display help text at the bottom
        window.clear_lines(y + 1)
        x = 0
        window.addstr(y + 2, x, 'Press \'q\' to quit.')

        # Clear the bottom 2 lines in case rows were moved up
        window.clear_lines(y + 3, lines=2)

    #function
    char = ''
    while char!='q':
        try:
            draw(departures)
        except RuntimeWarning:
            pass
        except RuntimeError as error:
            window.endwin()
            print(error)
            exit(1)

        char = window.getch()
    window.endwin()

