## Qt
import profile
import re
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QComboBox, QCheckBox, 
                                QDialog, QGroupBox, QHBoxLayout, 
                                QLabel, QLineEdit, QPushButton, 
                                QVBoxLayout, QWidget, QTabWidget,
                                QGridLayout, QFrame, QListWidget,
                                QMenu, QAbstractItemView)
from PySide6.QtGui import (QContextMenuEvent, QAction)

##>> Standard Python libraries. Do not need to bundle with the source code.
import sys
import site
import time
import json
import uuid
import random
import threading

site.addsitedir('./deps')

##>> Our deps folder
import mouse
import keyboard
import dpath.util as util


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
            "ButtonsConfig": {
                "MB1": True, 
                "MB2": False, 
                "MB3": False
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
        profile = self.Default
        self.Load()

    def Load(self):
        self.Profiles = json.load(open("./deps/profiles.json", "r"))
        self.SwitchProfile(None)
    def Save(self):
        # print(self.Profiles)
        ##print(f"Saving {json.dumps(self.Profiles[profile], indent=4)}")
        json.dump(self.Profiles, open("./deps/profiles.json", "w+"), indent = 2, separators = (', ', ': ')) ## Convert dictionary to JSON string, beautify, and write to file.

    def PerformClickConfigOverwrite(self, ConfigClass, name, value):
        self.Profiles[profile]["ClickConfig"][ConfigClass][name] = value

    def PerformButtonsConfigOverwrite(self, name, value):
        ##print(name, value)
        self.Profiles[profile]["ButtonsConfig"][name] = value
        # print(self.Profiles[profile])

    def SwitchProfile(self, Profile):
        profile = (Profile and (self.Profiles[Profile] and Profile) or (self.Profiles["Default"] and "Default")) or 0

    def PassDownArray(self, dict, array, v):
        # print(dict,array,v)
        d = dict[array[0]]
        # print(len(array), d)
        newarr = array
        ard = array
        newarr.pop(0)
        # print(len(newarr), len(ard))
        if len(newarr) == 0:
            d = v
        else:
            d = self.PassDownArray(d, newarr, v)
            dict[array[0]] = d
        return d           
    
    def PathToArray(self, path):
        pathArray = path.split("/")
        monolithic = self.Profiles[profile]
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
            # else:            
                # print (path + "/" + index,": ",value)
        return root

    def GetChildren(self, path):
        path = path or ""
        parent = self.PathToArray(path)
        children = {}
        for index, value in parent.items():
            # print (path + "/" + index,": ",value)
            children[index] = value
        return children

class __Settings__:
    def __init__(self):
        self.Settings = None
        self.Load()

    def Load(self):
        self.Settings = json.load(open("./deps/settings.json", "r"))
    def Save(self):
        # print(f"Saving {self.Profiles[profile]['ClickConfig']}")
        json.dump(self.Profiles, open("./deps/profiles.json", "w+"), indent = 2, separators = (', ', ': ')) ## Convert dictionary to JSON string, beautify, and write to file.

    def UpdateSettings(self, ConfigClass, name, value):
        self.Profiles[profile]["ClickConfig"][ConfigClass][name] = value

lmao = __Autoclicker__()
##lmao.CreateThread()
##time.sleep(1)
##lmao.Off()
##lmao.CreateThread()
##time.sleep(1)
##lmao.CreateThread()
##time.sleep(0.5)

##>>  The Qt Window class.

# class __Advanced__(QWidget):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.advanced_layout = QVBoxLayout()
#         self.ButtonsConfig()
#         self.advanced_layout.addWidget(self._ButtonsConfig)
#         self.setLayout(self.advanced_layout)
#         self.setWindowTitle("Basic Layouts")

#     def ButtonsConfig(self):
#         self._ButtonsConfig = QGroupBox("Buttons configuration")
#         horizontal = QHBoxLayout()
#         for name, value in self.profiles.GetChildren("/ButtonsConfig").items():
#             horizontal.addWidget(QLabel(name))
#             path = f"/ButtonsConfig/{name}"
#             # print(f"Variable {path} Value {value} Type {type(value)}")
#             widget = QCheckBox()
#             state = Qt.CheckState.Unchecked
#             if value is None:
#                 widget.setEnabled(False)
#                 state = Qt.CheckState.Checked
#                 value = 2
#             elif value:
#                 value = 2
#                 state = Qt.CheckState.Checked
#             else:
#                 value = 0
                
#             widget.setCheckState(state)
#             widget.stateChanged.connect(lambda v, name=name: util.new(self.Profiles, f'{profile}/ButtonsConfig/{name}', v==2))
#             ##self.Profiles[profile]["ButtonsConfig"][name] = a)##self.profiles.PerformButtonsConfigOverwrite(name, v==2)) ##self.Profiles[profile]["ButtonsConfig"][name] = v==2
#             horizontal.addWidget(widget)
#         self._ButtonsConfig.setLayout(horizontal)

class __Bind__(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        keyboard.unhook_all()
        self.bind = [] # bind and bind.split("+") or []
        keyboard.on_press(lambda key: self.Binder(keyboard.get_hotkey_name([key.name])))

        self.bind_layout = QGridLayout()
        self.UI()
        self.setLayout(self.bind_layout)
        self.setWindowTitle("Bind Keys")

    def UI(self):
        
        self.bindLabel = QLabel("Press keys...")
        self.bindLabel.setAlignment(Qt.AlignHCenter)
        save = QPushButton(f"Save")
        reset = QPushButton(f"Reset")
        delete = QPushButton(f"Delete")
        self.bind_layout.addWidget(self.bindLabel,    1, 1, 1, 3)
        self.bind_layout.addWidget(save,    2, 1, 1, 1)
        self.bind_layout.addWidget(reset,   2, 2, 1, 1)
        self.bind_layout.addWidget(delete,  2, 3, 1, 1)
        save.clicked.connect(self.Save)
        reset.clicked.connect(self.Reset)
        delete.clicked.connect(self.Delete)

    def Binder(self, key):
        if not(key in self.bind):
            if self.bind == ['']:
                self.bind = [key]
            else:
                self.bind.append(key)
            self.bind.sort(key=len, reverse=True)
        # print(key)
        # print(self.bind)
        
        # print("+".join(self.bind))
        self.bindLabel.setText("+".join(self.bind))

    def Save(self):
        keyboard.unhook_all()
        self.done(0)
    def Reset(self):
        self.bindLabel.setText("Press keys...")
        self.bind = []
    def Delete(self):
        keyboard.unhook_all()
        self.done(1)
    def GetResult(self):
        return ("+".join(self.bind))

class __ContextMenu__(QContextMenuEvent):
    def __init__(self, event):
        menu = QMenu()
        menu.addAction('hello')

class Window(QDialog):
    def __init__(self):
        super().__init__()

        self.Profiles = json.load(open("./deps/profiles.json", "r"))
        self.autoclicker = __Autoclicker__()

        self.setLayout(self.ProfilesTabs())        
        self.setWindowTitle("Autoclicker")

    def Save(self):
        x = json.dump(self.Profiles, open("./deps/profiles.json", "w+"), indent = 2, separators = (', ', ': '))
        print("SAVED")
        print(x)
        print("FIN")

    def ProfilesTabs(self):
        tabsLayout = QVBoxLayout()
        tabs = QTabWidget()
        listOfProfiles = list(util.search(self.Profiles, '*').keys())
        for tabName in listOfProfiles:
            ##print(tabName)
            frame = QFrame()
            tabLayout = QVBoxLayout()
            topbar = QHBoxLayout()
            save = QPushButton(f"Save")
            save.clicked.connect(self.Save)
            topbar.addWidget(save)
            tabLayout.addLayout(topbar)
            tabLayout.addWidget(self.ClickConfigFrame(tabName))
            tabLayout.addWidget(self.KeybindsFrame(tabName))
            self.setLayout(tabLayout)
            frame.setLayout(tabLayout)
            tabs.addTab(frame, tabName)

        frame = QFrame()
        frame.setLayout(self.ManageProfilesFrame())
        tabs.addTab(frame, "Manage Profiles...")

        tabsLayout.addWidget(tabs)
        return tabsLayout

    def ManageProfilesFrame(self):
        layout = QVBoxLayout()
        profilesList = QListWidget()
        profilesList.addItems(list(util.search(self.Profiles, '*').keys()))
        profilesList.setDragDropMode(QAbstractItemView.InternalMove)
        profilesList.setDefaultDropAction(Qt.TargetMoveAction)
        profilesList.setContextMenuPolicy(Qt.ActionsContextMenu)
        profilesList.addAction("Hello")
        profilesList.addAction("test2")
        # profilesList.contextMenuEvent(__ContextMenu__, event)
        layout.addWidget(profilesList)
        return layout

    def ClickConfigFrame(self, profile):
        vertical = QVBoxLayout()
        # print(util.values(self.Profiles, f'{profile}/ClickConfig'))
        for ConfigClass in util.values(self.Profiles, f'{profile}/ClickConfig')[0].keys():
            horizontal = QHBoxLayout()
            horizontal.addWidget(QLabel(ConfigClass))
            # print(util.values(self.Profiles, f'{profile}/ClickConfig/{ConfigClass}'))
            for ConfigOption in util.values(self.Profiles, f'{profile}/ClickConfig/{ConfigClass}')[0]:
                value = util.values(self.Profiles, f'{profile}/ClickConfig/{ConfigClass}/{ConfigOption}')[0]
                match ConfigOption:
                    case "Value":
                        widget = QLineEdit()
                        widget.setText(value)
                        # print(ConfigClass, name, value)
                        widget.textChanged.connect(lambda v, ConfigClass=ConfigClass, name=ConfigOption: util.set(self.Profiles, f'{profile}/ClickConfig/{ConfigClass}/{name}', v))##self.profiles.PerformClickConfigOverwrite(ConfigClass, name, v))
                    case "Units":
                        widget = QComboBox()
                        widget.addItems(list(self.autoclicker.Units))
                        widget.setCurrentIndex(list(self.autoclicker.Units).index(value))
                        widget.currentIndexChanged.connect(lambda v, ConfigClass=ConfigClass, name=ConfigOption: util.set(self.Profiles, f'{profile}/ClickConfig/{ConfigClass}/{name}', list(self.autoclicker.Units)[v]))##self.profiles.PerformClickConfigOverwrite(ConfigClass, name, list(self.autoclicker.Units)[v]))
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
                        widget.stateChanged.connect(lambda v, ConfigClass=ConfigClass, name=ConfigOption: util.set(self.Profiles, f'{profile}/ClickConfig/{ConfigClass}/{name}', v==2))##self.profiles.PerformClickConfigOverwrite(ConfigClass, name, v==2))
                horizontal.addWidget(widget)
            vertical.addLayout(horizontal)
        ClickConfigFrame = QGroupBox("Click configuration")
        ClickConfigFrame.setLayout(vertical)
        return ClickConfigFrame

    def KeybindsFrame(self, profile):
        tabs = QTabWidget()
        tabsLayout = QGridLayout()
        for tabName in util.values(self.Profiles, f'{profile}/Keybinds')[0].keys():
            frameLayout = QGridLayout()
            i = 0
            for group in util.values(self.Profiles, f'{profile}/Keybinds/{tabName}')[0].keys():
                i += 1
                frame = QGroupBox(group)
                layout = QVBoxLayout()
                layout.setAlignment(Qt.AlignTop)
                for bind in util.values(self.Profiles, f'{profile}/Keybinds/{tabName}/{group}')[0]:
                    if bind:
                        bindButton = QPushButton(f"{bind}")
                        bindButton.clicked.connect(lambda x=True, path=f'{profile}/Keybinds/{tabName}/{group}', layout=layout, bindButton=bindButton: self.BindHandler(path, layout, bindButton))
                        layout.addWidget(bindButton)

                bindButton = QPushButton("New...")
                bindButton.clicked.connect(lambda x=True, path=f'{profile}/Keybinds/{tabName}/{group}', layout=layout, bindButton=bindButton: self.BindHandler(path, layout, bindButton))
                layout.addWidget(bindButton)
                
                frame.setLayout(layout)
                frameLayout.addWidget(frame, i//3, (i-1)%2)

            wid = QFrame()
            wid.setLayout(frameLayout)
            tabs.addTab(wid, tabName)
        tabsLayout.addWidget(tabs)
        KeybindsFrame = QGroupBox("Keybinds")
        KeybindsFrame.setLayout(tabsLayout)
        return KeybindsFrame

    def BindHandler(self, path, layout, bindButton):
        bind = bindButton.text()
        if bind == "New...":
            bind = None
        binder = __Bind__(self)
        result = binder.exec()

        if result == 0:
            value = binder.GetResult() or bind
            util.new(self.Profiles, f"{path}/{bind}", value)
            bindButton.setText(f"{value}")
            if bind is None:
                newBindButton = QPushButton("New...")
                newBindButton.clicked.connect(lambda x=True, path=path, layout=layout, bindButton=bindButton, bind=None: self.BindHandler(path, layout, newBindButton))
                layout.addWidget(newBindButton)
        elif result == 1 and bind is not None:
                util.new(self.Profiles, f"{path}/{bind}", None)
                bindButton.deleteLater()
        else:
            assert("Invalid BindHandler code")

        print(json.dumps(self.Profiles, indent=4, sort_keys=True))
        # print(self.layout())
        # # self.WipeWidget(self.layout())
        # self.layout().deleteLater()
        # self.setLayout(QGridLayout())
        # print(self.layout())
        # print("PERFORING reload")
        # # self.setLayout(self.ProfilesTabs())   
        # print("reloadlded")
    
    def WipeWidget(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.WipeWidget(child.layout())
        layout.deleteLater()

##>>  Initialise the app and create the window.

app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()
##sys.exit(window.exec())