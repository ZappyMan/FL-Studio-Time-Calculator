# --------------------------------------------
#   Version: 1.0
#   Creators: Elliott Chimienti, Zane Little
#   Support us!: https://ko-fi.com/flhourcounterguys
# -------------------------------------------

import FLP, struct, glob, os, fnmatch, sys, gc
import winerror
import win32api
import win32job
import PySimpleGUI as sg
import webbrowser
from datetime import datetime,timedelta,date
import os.path
from FLP import FLPFile
from sys import argv


g_hjob = None
def mprint(*args, **kwargs):
    window['-ML-'].print(*args, **kwargs)
print = mprint

# -------- WINDOWS MEMORY MANAGEMENT -----------------
def create_job(job_name='', breakaway='silent'):
    hjob = win32job.CreateJobObject(None, job_name)
    if breakaway:
        info = win32job.QueryInformationJobObject(hjob,
                    win32job.JobObjectExtendedLimitInformation)
        if breakaway == 'silent':
            info['BasicLimitInformation']['LimitFlags'] |= (
                win32job.JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK)
        else:
            info['BasicLimitInformation']['LimitFlags'] |= (
                win32job.JOB_OBJECT_LIMIT_BREAKAWAY_OK)
        win32job.SetInformationJobObject(hjob,
            win32job.JobObjectExtendedLimitInformation, info)
    return hjob

def assign_job(hjob):
    global g_hjob
    hprocess = win32api.GetCurrentProcess()
    try:
        win32job.AssignProcessToJobObject(hjob, hprocess)
        g_hjob = hjob
    except win32job.error as e:
        if (e.winerror != winerror.ERROR_ACCESS_DENIED or
            sys.getwindowsversion() >= (6, 2) or
            not win32job.IsProcessInJob(hprocess, None)):
            raise
        warnings.warn('The process is already in a job. Nested jobs are not '
            'supported prior to Windows 8.')

def limit_memory(memory_limit):
    if g_hjob is None:
        return
    info = win32job.QueryInformationJobObject(g_hjob,
                win32job.JobObjectExtendedLimitInformation)
    info['ProcessMemoryLimit'] = memory_limit
    info['BasicLimitInformation']['LimitFlags'] |= (
        win32job.JOB_OBJECT_LIMIT_PROCESS_MEMORY)
    win32job.SetInformationJobObject(g_hjob,
        win32job.JobObjectExtendedLimitInformation, info)

# -------------------------------------------------------
# Reverses endian. Ex: "hello!" = "o!llhe"
def reverse_endian(hex):
    final = ''
    i=0
    while i < len(hex)/2:
        final = (hex[i*2] + hex[i*2+1]) + final
        i = i + 1
    return final

# Returns string with flp hex time
def get_hex(track):
    track.parse()
    track = str(track)
    idx = track.find('(ProjectTime) =') + 16
    return track[idx:idx+48]

# Cleans string and converts to float
def clean_convert(hex):
    hex = hex.strip()    # remove any lingering returns
    hex = hex.replace(" ","")     # remove all spaces
    hex = reverse_endian(hex)
    hex = hex[0:16]
    return struct.unpack("d", struct.pack("Q",int("0x"+hex, 16)))[0] # convert hex string to float!

# cleans string for time conversion
def hex_time(hex):
    hex = hex.strip()    # remove any lingering returns
    hex = hex.replace(" ","")     # remove all spaces
    hex = reverse_endian(hex)
    hex = hex[16:32]
    hex = struct.unpack("d", struct.pack("Q",int("0x"+hex, 16)))[0]
    return datetime(1899 ,12,30) + timedelta(days=hex)

# GUI-----------------------------------------------------------
if __name__ == "__main__":

    sg.theme('Dark')
    # Define window layout
    layout = [[sg.MLine(size=(54,15), key='-ML-', disabled = True, write_only = True, no_scrollbar = True, auto_refresh = True)],
                [sg.Text('Select Time Frame (Leave blank for all time)')],
                [sg.In('Earliest',disabled = True,text_color = '#737373',size=(23,1)), sg.Text(' to '),sg.In('Latest',disabled = True,text_color = '#737373',size=(23,1))],
                [sg.CalendarButton('Start Date', target=(2,0), key='date1'), sg.Text('                             '),sg.CalendarButton('End Date', target=(2,2), key='date2')],
                [sg.Text('')],
                [sg.Text('Select Master Folder')],
                [sg.In('No Folder Selected',disabled = True,text_color = '#737373'), sg.FolderBrowse(initial_folder = 'C:',key = "SelectedFolder")],
                [ sg.Button('About',button_color='#52829c'), sg.Text('                    '), sg.Button('Calculate!')]
             ]


    # Create WINDOWS
    window = sg.Window('FL Studio Time Calculator', layout, grab_anywhere=True)
    # GUI Loop
    while True:
        event, values = window.read()   # Read the event that happened and the values dictionary
        if event == sg.WIN_CLOSED or event == 'Exit':     # If user closed window with X or if user clicked "Exit" button then exit
         window.close()
         break

        if event == 'Calculate!':
            if values[2] == 'No Folder Selected':
                sg.Popup('Error, no folder selected', keep_on_top=True)
            else:
                if values[0] == 'Earliest':
                    date2 = date(1997, 12, 18)
                else:
                    date2 =  datetime.date(datetime.fromisoformat(values[0]))

                if values[1] == 'Latest':
                    date1 = datetime.date(datetime.now())
                else:
                    date1 = datetime.date(datetime.fromisoformat(values[1]))
                window['-ML-'].update('')
                if(date2 > datetime.date(datetime.now())):
                    print("     ----------------------------------------------")
                    print("     ",date2, " Hasn't Happened Yet!")
                    print("     ----------------------------------------------")
                elif(date2 > date1):
                    print("     ----------------------------------------------")
                    print("     Make Sure Start Date Is Before End Date")
                    print("     ----------------------------------------------")
                else:
                    assign_job(create_job())
                    memory_limit = 1000 * 1024 * 1024 # 1000 MiB
                    limit_memory(memory_limit)  # enact memory limit
                    total = 0   # will store total time
                    totalfiles=0

                    everything = glob.glob(values[2]+"/**/*.flp", recursive=True)
                    if not everything:                              # Checks if list is empty, no flps found
                        sg.Popup('Error, no FLP files found', keep_on_top=True)
                    else:
                        print("Scanning",values['SelectedFolder'],"for project files. This may take a moment!")
                        directory = values[2].replace("\\","/")
                        for thing in everything:        # for every "flp" file
                            thing = thing.replace("\\","/") # idk why this isnt already happening within glob
                            x = FLPFile(thing)
                            x.parse()
                            for idx, track in enumerate(x):
                                track.parse() # this sucks
                                window['-ML-'].update("Found file: "+thing.replace(directory+'/',''))
                                print("\nTotal found: "+str(totalfiles))
                                hex = get_hex(track)
                                cur = datetime.date(hex_time(hex))
                                if cur >= date2 and cur <= date1:
                                    total += clean_convert(hex)
                                    totalfiles+=1
                                del track           # clear parsed memory
                                gc.collect()

                        window['-ML-'].update('')
                        if totalfiles == 0:
                            print("     ----------------------------------------------")
                            print("     No Project Files Found Within Date Range :(")
                            print("     ----------------------------------------------")
                        else:
                            # Stats calculations
                            total = str(total)
                            days = total[0:total.find(".")]
                            hours = str((86400 * (float(total) - float(days)))/3600)
                            totalhours = str(float(days) * 24 + float(hours))
                            totalhours = round(float(totalhours),2)
                            temp = hours
                            hours = hours[0:hours.find(".")]
                            min = (float(temp) - float(hours))*60
                            min = round(float(min),1)
                            averagehours = str(round(float(totalhours)/float(totalfiles),2))

                            print()
                            print("     Howdy",os.getlogin()+"!")
                            print("     It is",date.today())
                            print()
                            print("     Your FL Studio Stats For ", date2 , " to ", date1)
                            print("     ----------------------------------------------")
                            print("     Total Project Files:",totalfiles)
                            print("     -")
                            print("     Total Active Time:",days,"day(s),", hours,"hours, and",min,"minutes!")
                            print("     -")
                            print("     Total Active Hours:",totalhours)
                            print("     -")
                            print("     Average Hours Per Project:",averagehours)
                            print("     ----------------------------------------------")
                            window.Refresh()
        elif event == 'About':
            layout2 = [[sg.Text('Developed by: Elliott Chimienti & Zane Little')],
                        [sg.Text('FL Studio keeps track of how many active hours you spend on each project, but not your total time in the program. \nWith this application, you can finally see your total hours without having to open up all your files and adding everything together! \nIdle time is still not accounted for, so the time this program displays to you only shows your active working hours. \nYou may also select dates for the program to search between, say, if you wanted to see how many hours you spent on FL in a given month (or whatever time frame you like)!\n')],
                        [sg.Text('This program was created out of the primal, human urge to keep track of and gawk at the amount of time we all spend on FL Studio. \nFor better or for worse, we will never stop producing!')],
                        [sg.Button('Support Us!',button_color='#d1b000'), sg.Button('Exit')]]
            pop = sg.Window('About', layout2, grab_anywhere=True)
            while True:
                event2, values2 = pop.read()
                if event2 == sg.WIN_CLOSED or event2 == 'Exit':     # If user closed window with X or if user clicked "Exit" button then exit
                    pop.close()
                    break
                elif event2 == 'Support Us!':
                    webbrowser.open(r'https://ko-fi.com/flhourcounterguys')
                pop.refresh()
