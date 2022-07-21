## Qt
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QComboBox, QCheckBox, 
                                QDialog, QGroupBox, QHBoxLayout, 
                                QLabel, QLineEdit, QPushButton, 
                                QVBoxLayout)
##>> Standard Python libraries. Do not need to bundle with the source code.
import sys
import time
import json
import uuid
import random
import threading
##>> Our deps folder
import deps.mouse as mouse
import deps.keyboard as keyboard
import deps.profilemenu as profilemenu


class __Autoclicker__:
    def __init__(self):
        self.Units = {"Milliseconds": 0.001, "Seconds": 1, "Minutes": 60, "Hours": 3600}
        self.NewUUID = uuid.uuid4
        class __Thread__:
            def __init__(self):
                self.Instance = None
                self.UUID =  None
                self.Count = 0
        
        self.Thread = __Thread__()

        self.Clicks = 0

    def Autoclicker(self):
        LocalUUID = self.Thread.UUID
        self.Thread.Count += 1
        LocalThreadCount = self.Thread.Count
        while self.Thread.UUID == LocalUUID:
            self.Clicks += 1
            time.sleep(0.5)
            print(f"Click: {self.Clicks} Thread Numerator: {LocalThreadCount} Thread UUID: {LocalUUID}")

    def CreateThread(self):
        if not self.Thread.Instance:
            self.Thread.UUID = self.NewUUID()
            self.Thread.Instance = threading.Thread(target = self.Autoclicker, daemon = True, name = self.Thread.UUID)
            self.Thread.Instance.start()

    def On(self):
        self.CreateThread()

    def Off(self):
        self.Thread.UUID = self.NewUUID()
        self.Thread.Instance = None
    
    def Toggle(self):
        if self.Thread.Instance:
            self.Off()
        else:
            self.On()

class __Profiles__:
    def __init__(self):
        self.Default = {
            "ClickInterval": {
                "SleepInterval": {
                    "Value": 10,
                    "Units": "Milliseconds",
                    "Enabled": True
                },
                "HoldInterval": {
                    "Value": 20,
                    "Units": "Milliseconds",
                    "Enabled": True
                },
                "RandomInterval": {
                    "Value": 30,
                    "Units": "Milliseconds",
                    "Enabled": True
                }
            }, 
            "Keybinds": {
                "key_press": {
                    "toggle": ["F6"],
                    "on": [],
                    "off": [],
                    "open": []
                },
                "hotkey": {
                    "toggle": [],
                    "on": [],
                    "off": ["alt+tab", "esc", "ctrl+alt+del"],
                    "open": []
                }
            }
        }
        self.Profiles = None ## TODO PLS
        self.Profile = self.Default
        self.Load()

    def Load(self):
        self.Profiles = json.load(open("./deps/profiles.json", "r"))
        self.SwitchProfile(None)
    def Save(self):
        print(f"Saving {self.Profiles[self.Profile]['ClickConfig']}")
        json.dump(self.Profiles, open("./deps/profiles.json", "w+"), indent = 2, separators = (', ', ': ')) ## Convert dictionary to JSON string, beautify, and write to file.

    def PerformClickConfigOverwrite(self, ConfigClass, name, value):
        self.Profiles[self.Profile]["ClickConfig"][ConfigClass][name] = value

    def SwitchProfile(self, Profile):
        self.Profile = (Profile and (self.Profiles[Profile] and Profile) or (self.Profiles["Default"] and "Default")) or 0

    def PassDownArray(self, dict, array, v):
        print(dict,array,v)
        d = dict[array[0]]
        print(len(array), d)
        newarr = array
        ard = array
        newarr.pop(0)
        print(len(newarr), len(ard))
        if len(newarr) == 0:
            d = v
        else:
            d = self.PassDownArray(d, newarr, v)
            dict[array[0]] = d
        return d           

    def SaveFromPath(self, path, v):
        pathArray = path.split("/")
        while("" in pathArray) :
            pathArray.remove("")
        ##ret = self.PassDownArray(self.Profiles[self.Profile], pathArray, v)
        self.Profiles[self.Profile][pathArray] = v## = ret
        print(self.Profiles)
        print(v)
    
    def PathToArray(self, path):
        pathArray = path.split("/")
        monolithic = self.Profiles[self.Profile]
        for value in pathArray:
            if len(value) > 0:
                monolithic = monolithic[value]
        return monolithic

    def GetDescendants(self, path):
        path = path or ""
        parent = self.ConvertPath(path)
        root = []
        for index, value in parent.items():        
            if isinstance(value, dict):
                for directory in self.Iterate(path + "/" + index):
                    root.append(directory)
            else:            
                print (path + "/" + index,": ",value)
        return root

    def GetChildren(self, path):
        path = path or ""
        parent = self.PathToArray(path)
        children = {}
        for index, value in parent.items():
            print (path + "/" + index,": ",value)
            children[index] = value
        return children

lmao = __Autoclicker__()
##lmao.CreateThread()
##time.sleep(1)
##lmao.Off()
##lmao.CreateThread()
##time.sleep(1)
##lmao.CreateThread()
##time.sleep(0.5)

##>>  The Qt Window class.

class Window(QDialog):
    def __init__(self):
        super().__init__()

        self.profiles = __Profiles__()
        self.autoclicker = __Autoclicker__()
        self.profiles.Load()

        topbar = QHBoxLayout()
        settings = QPushButton(f"Settings")
        topbar.addWidget(settings)

        def callback(v):
            pass

        widget = QComboBox()
        widget.addItems(self.profiles.Profiles.keys())
        widget.setCurrentIndex(0)
        widget.currentIndexChanged.connect(callback)
        topbar.addWidget(widget)

        save = QPushButton(f"Save")
        save.clicked.connect(self.profiles.Save)
        topbar.addWidget(save)

        main_layout = QVBoxLayout()
        main_layout.addLayout(topbar)
        self.ClickConfigFrame()
        main_layout.addWidget(self._ClickConfigFrame)
        self.setLayout(main_layout)

        self.setWindowTitle("Basic Layouts")

    def ClickConfigFrame(self):
        self._ClickConfigFrame = QGroupBox("Click configuration")
        vertical = QVBoxLayout()
        for ConfigClass, ConfigOption in self.profiles.GetChildren("/ClickConfig").items():
            horizontal = QHBoxLayout()
            horizontal.addWidget(QLabel(ConfigClass))
            for name, value in ConfigOption.items():
                ## print(f"Class: {ConfigClass} Option: {ConfigOption} Name: {name} Value: {value} Type: {type(value)}")
                path = f"/ClickConfig/{ConfigClass}/{name}"
                print(f"Variable {path} Value {value} Type {type(value)}")

                match name:
                    case "Value":
                        widget = QLineEdit()
                        widget.setText(value)
                        print(ConfigClass, name, value)
                        widget.textChanged.connect(lambda v, ConfigClass=ConfigClass, name=name: self.profiles.PerformClickConfigOverwrite(ConfigClass, name, v))
                    case "Units":
                        widget = QComboBox()
                        widget.addItems(list(self.autoclicker.Units))
                        widget.setCurrentIndex(list(self.autoclicker.Units).index(value))
                        widget.currentIndexChanged.connect(lambda v, ConfigClass=ConfigClass, name=name: self.profiles.PerformClickConfigOverwrite(ConfigClass, name, list(self.autoclicker.Units)[v]))
                    case "Enabled":
                        widget = QCheckBox()
                        state = Qt.CheckState.Unchecked
                        if value is None:
                            widget.setEnabled(False)
                            state = Qt.CheckState.Checked
                            value = 2
                        elif value:
                            value = 2
                            state = Qt.CheckState.Checked
                        else:
                            value = 0
                            
                        widget.setCheckState(state)
                        widget.stateChanged.connect(lambda v, ConfigClass=ConfigClass, name=name: self.profiles.PerformClickConfigOverwrite(ConfigClass, name, v==2))
                horizontal.addWidget(widget)
            vertical.addLayout(horizontal)
        self._ClickConfigFrame.setLayout(vertical)

##>>  Initialise the app and create the window.

app = QApplication(sys.argv)
window = Window()
sys.exit(window.exec())