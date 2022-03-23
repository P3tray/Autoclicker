print("[INFO] Starting autoclicker.")
version = "V0.2"

###########################
##  Importing libraries  ##
###########################

from typing import Literal
import deps.keyboard as keyboard
import deps.mouse as mouse
import deps.profilemenu as profilemenu
import time
import datetime
import tkinter as tk
import json
import random
from threading import Thread
from tkinter import ttk


###################################
##  Default setting.json values  ##
###################################

time_to_hold = 1
time_to_sleep = 1

#####################################
##  Other globals used throughout  ##
#####################################

num_of_clicks = 0
run_autoclicker = False
autoclicker_thread = None

#################################
##  Initialise Tkinter Window  ##
#################################
window = tk.Tk()
window.title('Autoclicker')
##window.geometry('300x300')

window.resizable(0, 0)
window.style = ttk.Style(window)
try:
    window.iconbitmap("./deps/icon.ico") 
    window.style.theme_use("vista")
except:
    pass
################################
##  Status bar at the bottom  ##
################################

StatusBar = ttk.Label(window, text = 'Autoclicker [' + version + '] MIT ' + str(datetime.date.today().year), relief = "flat")
##StatusBar.config(bg = "gray51", fg = "white")
StatusBar.grid(row = 5, column = 1, columnspan = 2, padx = 10, pady = 5, ipadx = 10, ipady = 5, sticky = "w")

#################################
##  Variables used by tkinter  ##
#################################

Profile = tk.StringVar()
SleepInterval = tk.StringVar()
Unit_SleepInterval = tk.StringVar()
HoldInterval = tk.StringVar()
Unit_HoldInterval = tk.StringVar()
HoldIntervalEnabled = tk.BooleanVar()
RandomInterval = tk.StringVar()
Unit_RandomInterval = tk.StringVar()
RandomIntervalEnabled = tk.BooleanVar()


######################################
##  Load settings.json and profile  ##
######################################

settingsJson = json.load(open("./deps/settings.json", "r"))
Profile.set(list(settingsJson)[0])
settings = settingsJson[Profile.get()]

####################################
##  Functions used by the window  ##
####################################

def UnitsToMath(string):
    ## Yes, I know I can use a table, no, I can't be bothered to.
    ## Yes, I know it will still be unoptimised despite a table.
    ## No, I wouldn't be bothered to optimise it further than that.
    if string  == "Milliseconds":
        return 0.001
    elif string  == "Seconds":
        return 1
    elif string  == "Minutes":
        return 60
    elif string  == "Hours":
        return 3600
    ## Cases below are redundant due to an overflow in time.sleep()
    elif string  == "Days":
        return 86400
    elif string == "Weeks":
        return 604800

def LoadSettings(newProfile):
    global settings
    if newProfile  == "New profile...":
        ProfileCreation = tk.Toplevel(window)
        ProfileCreation.title('New Profile Creation')
        ProfileCreation.resizable(0, 0)
        ProfileCreation.style = ttk.Style(window)
        ProfileCreation.style.theme_use("vista")
        ProfileCreation.iconbitmap("./deps/icon.ico")

        Title_ProfileCreation = ttk.Label(ProfileCreation, text = 'Please input a name for the new profile:')
        Title_ProfileCreation.grid(row = 1, column = 1, columnspan = 2, padx = 5, pady = 5)
        Item_ProfileCreation = ttk.Entry(ProfileCreation, textvariable = Profile)
        Item_ProfileCreation.grid(row = 2, column = 1, columnspan = 2, padx = 5, pady = 5)
        def save():
            SaveSettings()
            LoadSettings(Profile.get())
            Item_Profile = ttk.OptionMenu(window, Profile, Profile.get(), *list(settingsJson), "New profile...", command = LoadSettings)
        def cancel():
            ProfileCreation.destroy()
        ProfileCreation_Cancel = ttk.Button(ProfileCreation, text = "Cancel", command = cancel)
        ProfileCreation_Cancel.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = "e")
        ProfileCreation_Save = ttk.Button(ProfileCreation, text = "Save", command = save, takefocus = True)
        ProfileCreation_Save.grid(row = 3, column = 2, padx = 5, pady = 5, sticky = "w")
    profilemenu.createMenu(newProfile, list(settingsJson))
    settings = settingsJson[newProfile]
    SleepInterval.set(settings["ClickInterval"].get("SleepInterval", "0"))
    Unit_SleepInterval.set(settings["ClickInterval"].get("Unit_SleepInterval", "Milliseconds"))
    HoldInterval.set(settings["ClickInterval"].get("HoldInterval", "0"))
    Unit_HoldInterval.set(settings["ClickInterval"].get("Unit_HoldInterval", "Milliseconds"))
    HoldIntervalEnabled.set(settings["ClickInterval"].get("HoldIntervalEnabled", False))
    RandomInterval.set(settings["ClickInterval"].get("RandomInterval", "0"))
    Unit_RandomInterval.set(settings["ClickInterval"].get("Unit_RandomInterval", "Milliseconds"))
    RandomIntervalEnabled.set(settings["ClickInterval"].get("RandomIntervalEnabled", False))

    keyboard.unhook_all() ## This method is the best I've ever seen.

    for i,v in settings["toggle_autoclicker_on_press_key"].items():
        keyboard.on_press_key(v, lambda key: toggle_autoclicker())
    for i,v in settings["toggle_autoclicker_on_hotkey"].items():
        keyboard.add_hotkey(v, lambda: toggle_autoclicker())
    for i,v in settings["turn_off_autoclicker_on_press_key"].items(): 
        keyboard.on_press_key(v, lambda key: turn_off_autoclicker())
    for i,v in settings["turn_off_autoclicker_on_hotkey"].items(): 
        keyboard.add_hotkey(v, lambda: turn_off_autoclicker())
    for i,v in settings["toggle_open_autoclicker_on_press_key"].items():
        keyboard.on_press_key(v, lambda key: window.quit())
    for i,v in settings["toggle_open_autoclicker_on_hotkey"].items():
        keyboard.add_hotkey(v, lambda: window.quit())

    StatusBar.configure(text = "Loaded " + Profile.get())

def SaveSettings():
    global settings
    settings["ClickInterval"]["SleepInterval"] = SleepInterval.get()
    settings["ClickInterval"]["Unit_SleepInterval"] = Unit_SleepInterval.get()
    settings["ClickInterval"]["HoldInterval"] = HoldInterval.get()
    settings["ClickInterval"]["Unit_HoldInterval"] = Unit_HoldInterval.get()
    settings["ClickInterval"]["HoldIntervalEnabled"] = HoldIntervalEnabled.get()
    settings["ClickInterval"]["RandomInterval"] = RandomInterval.get()
    settings["ClickInterval"]["Unit_RandomInterval"] = Unit_RandomInterval.get()
    settings["ClickInterval"]["RandomIntervalEnabled"] = RandomIntervalEnabled.get()
    settingsJson[Profile.get()] = settings
    json.dump(settingsJson, open("./deps/settings.json", "w+"), indent = 2, separators = (',', ': ')) ## Convert dictionary to JSON string, beautify, and write to file.
    StatusBar.configure(text = "Saved " + Profile.get())

profilemenu = profilemenu.Menu(window, tk, ttk, LoadSettings)
LoadSettings(Profile.get())

###############################
##  Click Intervals (ROW 1)  ##
###############################
Frame_ClickIntervals = ttk.LabelFrame(window, text = "Click speed settings")
Frame_ClickIntervals.grid(row = 2, column = 1, columnspan = 2, padx = 10, pady = 5)

## SleepInterval
Title_SleepInterval = ttk.Label(Frame_ClickIntervals, text = 'Click interval ')
Title_SleepInterval.grid(row = 1, column = 1)
Item_SleepInterval = ttk.Entry(Frame_ClickIntervals, width = 4, textvariable = SleepInterval)
Item_SleepInterval.grid(row = 1, column = 2)
Item_Unit_SleepInterval = ttk.OptionMenu(Frame_ClickIntervals, Unit_SleepInterval,"Milliseconds","Milliseconds","Seconds","Minutes","Hours")
Item_Unit_SleepInterval.grid(row = 1, column = 3)
Item_SleepIntervalEnabled = ttk.Checkbutton(Frame_ClickIntervals, state = 'disabled', onvalue = True) ##, onvalue = True, offvalue = False
Item_SleepIntervalEnabled.grid(row = 1, column = 4)

## HoldInterval
Title_HoldInterval = ttk.Label(Frame_ClickIntervals, text = 'Hold interval ')
Title_HoldInterval.grid(row = 2, column = 1)
Item_HoldInterval = ttk.Entry(Frame_ClickIntervals, width = 4, textvariable = HoldInterval)
Item_HoldInterval.grid(row = 2, column = 2)
Item_Unit_HoldInterval = ttk.OptionMenu(Frame_ClickIntervals, Unit_HoldInterval,Unit_HoldInterval.get(),"Milliseconds","Seconds","Minutes","Hours")
Item_Unit_HoldInterval.grid(row = 2, column = 3)
Item_HoldIntervalEnabled = ttk.Checkbutton(Frame_ClickIntervals, variable = HoldIntervalEnabled) ##, onvalue = True, offvalue = False
Item_HoldIntervalEnabled.grid(row = 2, column = 4)

## RandomInterval
Title_RandomInterval = ttk.Label(Frame_ClickIntervals, text = 'Random interval ')
Title_RandomInterval.grid(row = 3, column = 1, pady = (0,5))
Item_RandomInterval = ttk.Entry(Frame_ClickIntervals, width = 4, textvariable = RandomInterval)
Item_RandomInterval.grid(row = 3, column = 2, pady = (0,5))
Item_Unit_RandomInterval = ttk.OptionMenu(Frame_ClickIntervals, Unit_RandomInterval,Unit_RandomInterval.get(),"Milliseconds","Seconds","Minutes","Hours")
Item_Unit_RandomInterval.grid(row = 3, column = 3, pady = (0,5))
Item_RandomIntervalEnabled = ttk.Checkbutton(Frame_ClickIntervals, variable = RandomIntervalEnabled) ##, onvalue = True, offvalue = False
Item_RandomIntervalEnabled.grid(row = 3, column = 4)



######################################
##  Click Options (ROW 2 COLUMN 1)  ##
######################################
##testframe = ttk.LabelFrame(window, text = "Click options")
##testframe.grid(row = 3, column = 1, padx = 10, pady = 5, sticky = "w")

################################
##  Save button (bottom row)  ##
################################
SaveButton = ttk.Button(window, text = "Save", command = SaveSettings)
SaveButton.grid(row = 5, column = 2, padx = 10, pady = 5, sticky = "e")

def autoclicker():
    time_to_sleep = int(''.join(x for x in SleepInterval.get() if x.isdigit())) * UnitsToMath(Unit_SleepInterval.get())
    time_to_hold = (HoldIntervalEnabled.get() and int(''.join(x for x in HoldInterval.get() if x.isdigit())) * UnitsToMath(Unit_HoldInterval.get())) or 0
    time_to_randomize = (RandomIntervalEnabled.get() and int(''.join(x for x in RandomInterval.get() if x.isdigit())) * UnitsToMath(Unit_RandomInterval.get())) or 0
    print(time_to_randomize)
    print("--------------------------------------------------------")
    print("-[INFO] Time to sleep: ", time_to_sleep)
    print("-[INFO] Time to hold: ", time_to_hold)
    print("-[INFO] Will hold?: ", HoldIntervalEnabled.get())
    print("-[INFO] Autoclicker configured to run?: ", run_autoclicker)
    print("--------------------------------------------------------")
    StatusBar.configure(text = "Status: Autoclicker " + ((run_autoclicker and "ON!") or "OFF!"))
    while run_autoclicker:
        mouse.press(button='left')
        time.sleep(time_to_hold)
        mouse.release(button='left')
        time.sleep(time_to_sleep)
        time.sleep(random.uniform(0,time_to_randomize))
    StatusBar.configure(text = "Status: Autoclicker OFF!")

def toggle_autoclicker():
    global run_autoclicker
    run_autoclicker = not run_autoclicker
    print("[WARN] Autoclicker state changed to", run_autoclicker)
    autoclicker_thread = Thread(target = autoclicker)
    autoclicker_thread.start()

def turn_off_autoclicker():
    global run_autoclicker
    run_autoclicker = False
    print("[WARN] Autoclicker forced to", run_autoclicker)

def toggle_open_autoclicker():
    print("[WARN] Autoclicker quitting via toggle_open_autoclicker")
    window.quit()

StatusBar.configure(text = 'Autoclicker [' + version + '] MIT ' + str(datetime.date.today().year))

print("[INFO] Finished initializing autoclicker.")
window.mainloop()
print("[INFO] Window closed. Exiting autoclicker.")