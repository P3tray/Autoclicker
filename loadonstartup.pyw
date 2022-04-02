#################################
##  One day I'll improve this  ##
#################################

###########################
##  Importing libraries  ##
###########################

print("[INFO] Starting LoadOnStartup.")
import deps.keyboard as keyboard
import json
import pathlib
import os

#####################
##  Load settings  ##
#####################

settingsFile = open("./deps/settings.json", "r")
settings = json.load(settingsFile)

isOpen = False

######################################################
##  Function which starts new Autoclicker instance  ##
######################################################

def toggle_open_autoclicker():
    if not isOpen:
        path = str(pathlib.PurePath(__file__).with_name("main.pyw"))
        print(path)
        os.startfile(path)

############################
##  Bind key to function  ##
############################

for i,v in settings["toggle_open_autoclicker_on_press_key"].items():
    keyboard.on_press_key(v, lambda key: toggle_open_autoclicker())
for i,v in settings["toggle_open_autoclicker_on_hotkey"].items():
    print(i,v)
    keyboard.add_hotkey(v, lambda: toggle_open_autoclicker())

############################
##  Dunno what this does  ##
############################

input("Press any key to terminate the program.")