print("[INFO] Starting autoclicker.")
version = "V0.4"

###########################
##  Importing libraries  ##
###########################

from typing import Literal
from wsgiref import validate
import autoclicker
import autoclicker.keyboard as keyboard
import autoclicker.mouse as mouse
import autoclicker.profilemenu as profilemenu
from autoclicker.ttkwidgets import DebugWindow
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
    window.iconbitmap("./autoclicker/icon.ico") 
    window.style.theme_use("vista")
except:
    pass

################################
##  Status bar at the bottom  ##
################################

StatusBar = ttk.Label(window, text = '  Autoclicker [' + version + '] MIT ' + str(datetime.date.today().year), relief = "flat")

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
##  Load Settings.json and profile  ##
######################################

SettingsJSON = json.load(open("./autoclicker/Settings.json", "r"))
Profile.set(list(SettingsJSON["Profiles"])[0])
Profiles = SettingsJSON["Profiles"][Profile.get()]
Settings = SettingsJSON["Settings"]

                    ####################################
                    ##  Functions used by the window  ##
                    ####################################

toggle_autoclicker_on_press_key = {}

###############################################
##  Keybind confirguration (ROW 2 COLUMN 1)  ##
###############################################
Frame_KeybindConfirguration = ttk.LabelFrame(window, text = "Keybinds")
Frame_KeybindConfirguration.grid(row = 3, column = 1, columnspan = 2, padx = 10, pady = (5, 8))

if Settings["Status Bar"] == True:
    StatusBar.grid(row = 6, column = 1, columnspan = 20, padx = 0, pady = 0, ipadx = 10, ipady = 2, sticky = "w")
    ##StatusBar.grid_forget()

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

def IsInterger(value):
    return value.isdigit()

IsInterger = window.register(IsInterger)

def LoadProfiles(newProfile):
    global Profiles
    if newProfile  == "New profile...":
        ProfileCreation = tk.Toplevel(window)
        ProfileCreation.title('New Profile Creation')
        ProfileCreation.resizable(0, 0)
        ProfileCreation.style = ttk.Style(window)
        ProfileCreation.style.theme_use("vista")
        ProfileCreation.iconbitmap("./autoclicker/icon.ico")

        Title_ProfileCreation = ttk.Label(ProfileCreation, text = 'Please input a name for the new profile:')
        Title_ProfileCreation.grid(row = 1, column = 1, columnspan = 2, padx = 5, pady = 5)
        Item_ProfileCreation = ttk.Entry(ProfileCreation, textvariable = Profile, width=34)
        Item_ProfileCreation.grid(row = 2, column = 1, columnspan = 2, padx = 5, pady = 0)
        def save():
            SaveProfiles()
            LoadProfiles(Profile.get())
            Item_Profile = ttk.OptionMenu(window, Profile, Profile.get(), *list(SettingsJSON["Profiles"]), "New profile...", command = LoadProfiles)
        def cancel():
            ProfileCreation.destroy()
        ProfileCreation_Cancel = ttk.Button(ProfileCreation, text = "Cancel", command = cancel)
        ProfileCreation_Cancel.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = "w")
        ProfileCreation_Save = ttk.Button(ProfileCreation, text = "Save", command = save, takefocus = True)
        ProfileCreation_Save.grid(row = 3, column = 2, padx = 5, pady = 5, sticky = "e")
    profilemenu.createMenu(newProfile, list(SettingsJSON["Profiles"]))
    Profiles = SettingsJSON["Profiles"][newProfile]
    SleepInterval.set(Profiles["ClickInterval"].get("SleepInterval", "0"))
    Unit_SleepInterval.set(Profiles["ClickInterval"].get("Unit_SleepInterval", "Milliseconds"))
    HoldInterval.set(Profiles["ClickInterval"].get("HoldInterval", "0"))
    Unit_HoldInterval.set(Profiles["ClickInterval"].get("Unit_HoldInterval", "Milliseconds"))
    HoldIntervalEnabled.set(Profiles["ClickInterval"].get("HoldIntervalEnabled", False))
    RandomInterval.set(Profiles["ClickInterval"].get("RandomInterval", "0"))
    Unit_RandomInterval.set(Profiles["ClickInterval"].get("Unit_RandomInterval", "Milliseconds"))
    RandomIntervalEnabled.set(Profiles["ClickInterval"].get("RandomIntervalEnabled", False))

    keyboard.unhook_all() ## This method is the best I've ever seen.
    for v in Frame_KeybindConfirguration.winfo_children():
        v.destroy()

    for i, v in Profiles["toggle_autoclicker_on_press_key"].items():
        toggle_autoclicker_on_press_key[i] = v
        entry = ttk.Entry(Frame_KeybindConfirguration, width = 6)
        entry.insert(0, v)
        entry.grid(row = i, column = 1, columnspan=2)
        keyboard.on_press_key(v, lambda key: toggle_autoclicker())

    for i, v in Profiles["toggle_autoclicker_on_hotkey"].items():
        keyboard.add_hotkey(v, lambda: toggle_autoclicker())
    for i, v in Profiles["turn_off_autoclicker_on_press_key"].items(): 
        keyboard.on_press_key(v, lambda key: turn_off_autoclicker())
    for i, v in Profiles["turn_off_autoclicker_on_hotkey"].items(): 
        keyboard.add_hotkey(v, lambda: turn_off_autoclicker())
    for i, v in Profiles["toggle_open_autoclicker_on_press_key"].items():
        keyboard.on_press_key(v, lambda key: window.quit())
    for i, v in Profiles["toggle_open_autoclicker_on_hotkey"].items():
        keyboard.add_hotkey(v, lambda: window.quit())

    StatusBar.configure(text = "  Loaded " + Profile.get())

def SaveProfiles():
    global Profiles
    Profiles["ClickInterval"]["SleepInterval"] = SleepInterval.get()
    Profiles["ClickInterval"]["Unit_SleepInterval"] = Unit_SleepInterval.get()
    Profiles["ClickInterval"]["HoldInterval"] = HoldInterval.get()
    Profiles["ClickInterval"]["Unit_HoldInterval"] = Unit_HoldInterval.get()
    Profiles["ClickInterval"]["HoldIntervalEnabled"] = HoldIntervalEnabled.get()
    Profiles["ClickInterval"]["RandomInterval"] = RandomInterval.get()
    Profiles["ClickInterval"]["Unit_RandomInterval"] = Unit_RandomInterval.get()
    Profiles["ClickInterval"]["RandomIntervalEnabled"] = RandomIntervalEnabled.get()
    SettingsJSON["Profiles"][Profile.get()] = Profiles
    json.dump(SettingsJSON, open("./autoclicker/Settings.json", "w+"), indent = 2, separators = (', ', ': ')) ## Convert dictionary to JSON string, beautify, and write to file.
    StatusBar.configure(text = "  Saved " + Profile.get())

def LoadSettings():
    SettingsWindow = tk.Toplevel(window)
    SettingsWindow.title('Settings')
    SettingsWindow.resizable(0, 0)
    SettingsWindow.style = ttk.Style(window)
    SettingsWindow.style.theme_use("vista")
    SettingsWindow.iconbitmap("./autoclicker/icon.ico")

    Title_SettingsWindow = ttk.Label(SettingsWindow, text = 'Available settings:')
    Title_SettingsWindow.grid(row = 1, column = 1, columnspan = 2, padx = 5, pady = 5, sticky="w")

    TempSettings = {}

    i = 1
    for v in list(SettingsJSON["Settings"]):
        i = i + 1
        VarType = type(SettingsJSON["Settings"][v])
        if VarType == bool:
            TempSettings[v] = tk.BooleanVar()
            TempSettings[v].set(SettingsJSON["Settings"][v])
            Title_CheckButton = ttk.Label(SettingsWindow, text = "Enable " + v + "?")
            Title_CheckButton.grid(row = i, column = 1, padx = 5, pady = 0)
            CheckButton = ttk.Checkbutton(SettingsWindow, variable = TempSettings[v]) ##, onvalue = True, offvalue = False
            CheckButton.grid(row = i, column = 2, padx = 5, pady = 0)
    def save():
        for v in list(TempSettings):
            SettingsJSON["Settings"][v] = TempSettings[v].get()
        json.dump(SettingsJSON, open("./autoclicker/Settings.json", "w+"), indent = 2, separators = (', ', ': ')) ## Convert dictionary to JSON string, beautify, and write to file.
        StatusBar.configure(text = "  Saved settings")
    def cancel():
        SettingsWindow.destroy()
    SettingsWindow_Cancel = ttk.Button(SettingsWindow, text = "Cancel", command = cancel)
    SettingsWindow_Cancel.grid(row = 100, column = 1, padx = 5, pady = 5, sticky = "w")
    SettingsWindow_Save = ttk.Button(SettingsWindow, text = "Save", command = save, takefocus = True)
    SettingsWindow_Save.grid(row = 100, column = 2, padx = 5, pady = 5, sticky = "e")

profilemenu = profilemenu.Menu(window, tk, ttk, LoadProfiles)
LoadProfiles(Profile.get())

###############################
##  Click Intervals (ROW 1)  ##
###############################
Frame_ClickIntervals = ttk.LabelFrame(window, text = "Click speed")
Frame_ClickIntervals.grid(row = 2, column = 1, columnspan = 2, padx = 10, pady = (5, 8))

Title_SleepInterval = ttk.Label(Frame_ClickIntervals, text = 'Click interval ')
Title_SleepInterval.grid(row = 1, column = 1)
Item_SleepInterval = ttk.Entry(Frame_ClickIntervals, width = 6, textvariable = SleepInterval, validate="key", validatecommand=(IsInterger, "%S"))
Item_SleepInterval.grid(row = 1, column = 2)
Item_Unit_SleepInterval = ttk.OptionMenu(Frame_ClickIntervals, Unit_SleepInterval, Unit_SleepInterval.get(), "Milliseconds", "Seconds", "Minutes", "Hours")
Item_Unit_SleepInterval.grid(row = 1, column = 3)
Item_SleepIntervalEnabled = ttk.Checkbutton(Frame_ClickIntervals, state = 'disabled', onvalue = True) ##, onvalue = True, offvalue = False
Item_SleepIntervalEnabled.grid(row = 1, column = 4)

## HoldInterval
Title_HoldInterval = ttk.Label(Frame_ClickIntervals, text = 'Hold interval ')
Title_HoldInterval.grid(row = 2, column = 1)
Item_HoldInterval = ttk.Entry(Frame_ClickIntervals, width = 6, textvariable = HoldInterval, validate="key", validatecommand=(IsInterger, "%S"))
Item_HoldInterval.grid(row = 2, column = 2)
Item_Unit_HoldInterval = ttk.OptionMenu(Frame_ClickIntervals, Unit_HoldInterval, Unit_HoldInterval.get(), "Milliseconds", "Seconds", "Minutes", "Hours")
Item_Unit_HoldInterval.grid(row = 2, column = 3)
Item_HoldIntervalEnabled = ttk.Checkbutton(Frame_ClickIntervals, variable = HoldIntervalEnabled) ##, onvalue = True, offvalue = False
Item_HoldIntervalEnabled.grid(row = 2, column = 4)

## RandomInterval
Title_RandomInterval = ttk.Label(Frame_ClickIntervals, text = 'Random interval ')
Title_RandomInterval.grid(row = 3, column = 1, pady = (0, 5))
Item_RandomInterval = ttk.Entry(Frame_ClickIntervals, width = 6, textvariable = RandomInterval, validate="key", validatecommand=(IsInterger, "%S"))
Item_RandomInterval.grid(row = 3, column = 2, pady = (0, 5))
Item_Unit_RandomInterval = ttk.OptionMenu(Frame_ClickIntervals, Unit_RandomInterval, Unit_RandomInterval.get(), "Milliseconds", "Seconds", "Minutes", "Hours")
Item_Unit_RandomInterval.grid(row = 3, column = 3, pady = (0, 5))
Item_RandomIntervalEnabled = ttk.Checkbutton(Frame_ClickIntervals, variable = RandomIntervalEnabled) ##, onvalue = True, offvalue = False
Item_RandomIntervalEnabled.grid(row = 3, column = 4)

def LoadKeybinds():
    pass


Title_test = ttk.Label(Frame_KeybindConfirguration, text = 'test')
Title_test.grid(row = 20, column = 1)


###################################################
##  Advanced options & Save button (bottom row)  ##
###################################################
SaveButton = ttk.Button(window, text = "Save", command = SaveProfiles)
SaveButton.grid(row = 1, column = 2, padx = 10, pady = (10, 0), sticky = "e")
SettingsButton = ttk.Button(window, text = "Settings", command = LoadSettings)
SettingsButton.grid(row = 1, column = 1, padx = 10, pady = (10, 0),  sticky = "w")

def autoclicker():
    time_to_sleep = int(SleepInterval.get()) * UnitsToMath(Unit_SleepInterval.get()) or 0
    time_to_hold = (HoldIntervalEnabled.get() and int(HoldInterval.get()) * UnitsToMath(Unit_HoldInterval.get())) or 0
    time_to_randomize = (RandomIntervalEnabled.get() and int(RandomInterval.get()) * UnitsToMath(Unit_RandomInterval.get())) or 0
    print("--------------------------------------------------------")
    print("-[INFO] Time to sleep: ", time_to_sleep)
    print("-[INFO] Time to hold: ", time_to_hold)
    print("-[INFO] Will hold?: ", HoldIntervalEnabled.get())
    print("-[INFO] Autoclicker configured to run?: ", run_autoclicker)
    print("--------------------------------------------------------")
    StatusBar.configure(text = "  Status: Autoclicker " + ((run_autoclicker and "ON!") or "OFF!"))
    while run_autoclicker:
        mouse.press(button='left')
        time.sleep(time_to_hold)
        mouse.release(button='left')
        time.sleep(time_to_sleep)
        time.sleep(random.uniform(0, time_to_randomize))
    StatusBar.configure(text = "  Status: Autoclicker OFF! ")

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

StatusBar.configure(text = '  Autoclicker [' + version + '] MIT ' + str(datetime.date.today().year))

print("[INFO] Finished initializing autoclicker.")
window.mainloop()
print("[INFO] Window closed. Exiting autoclicker.")