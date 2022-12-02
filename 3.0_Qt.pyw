##>> Qt
import profile
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
import os
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

# lmao = __Autoclicker__()
##lmao.CreateThread()
##time.sleep(1)
##lmao.Off()
##lmao.CreateThread()
##time.sleep(1)
##lmao.CreateThread()
##time.sleep(0.5)

class __KeyboardHandler__(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        # PySide6.QtWidgets.QTabWidget.currentChanged(index)
        # PySide6.QtWidgets.QTabWidget.currentIndex()
        # PySide6.QtWidgets.QTabWidget.tabText(index)
        # keyboard.add_hotkey(v, lambda: toggle_autoclicker()

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

class __Name__(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.nameLayout = QGridLayout()
        self.UI()
        self.setLayout(self.nameLayout)
        self.setWindowTitle("Name")

    def UI(self):
        
        self.nameLabel = QLabel("Please give a name...")
        self.nameLabel.setAlignment(Qt.AlignHCenter)
        self.name = QLineEdit()
        self.save = QPushButton(f"Save")
        self.nameLayout.addWidget(self.nameLabel,   1, 1, 1, 3)
        self.nameLayout.addWidget(self.name,        2, 1, 1, 2)
        self.nameLayout.addWidget(self.save,        2, 2, 1, 1)
        self.save.clicked.connect(self.Save)

    def Save(self):
        self.result = self.name.text()
        self.done(0)
    def GetResult(self):
        return self.result    

class Window(QDialog):
    def __init__(self):
        super().__init__()

        self.Profiles = json.load(open("./deps/profiles.json", "r"))
        self.autoclicker = __Autoclicker__()

        self.setLayout(self.ProfilesTabs())        
        self.setWindowTitle("Autoclicker")

    def Save(self):
        newJson = {}
        for x in range(self.profilesList.count()):
            i = self.profilesList.item(x).text()
            newJson[i] = self.Profiles[i]
        print("Saving self.Profiles to profiles.json")
        x = json.dump(newJson, open("./deps/profiles.json", "w+"), indent = 2, separators = (', ', ': '))
        print("Successfully completed in saving self.Profiles to profiles.json")

    def ProfilesTabs(self):
        tabsLayout = QVBoxLayout()
        self.tabs = QTabWidget()
        listOfProfiles = list(util.search(self.Profiles, '*').keys())
        for tabName in listOfProfiles:
            frame = QFrame()
            tabLayout = QVBoxLayout()
            topbar = QHBoxLayout()
            tabLayout.addLayout(topbar)
            tabLayout.addWidget(self.ClickConfigFrame(tabName))
            tabLayout.addWidget(self.KeybindsFrame(tabName))
            self.setLayout(tabLayout)
            frame.setLayout(tabLayout)
            self.tabs.addTab(frame, tabName)

        frame = QFrame()
        frame.setLayout(self.ManageProfilesFrame())
        self.tabs.addTab(frame, "Manage Profiles...")

        save = QPushButton(f"Save all changes")
        save.clicked.connect(self.Save)
        tabsLayout.addWidget(save)
        tabsLayout.addWidget(self.tabs)
        self.tabs.currentChanged.connect(self.BindAll)
        self.BindAll()
        return tabsLayout
    
    def ProfilesContextMenu(self, pos):
        if self.profilesList.count() == 0:
            return
        menu = QMenu(self)
        newProfileAction = menu.addAction("New profile...")
        renameProfileAction = menu.addAction("Rename profile...")
        deleteProfileAction = menu.addAction("Delete profile...")
        chosen_action = menu.exec(self.profilesList.viewport().mapToGlobal(pos))
        current_item = self.profilesList.currentItem()
        self.UnbindAll()

        if chosen_action == newProfileAction:
            print("New")
            name = __Name__(self)
            result = name.exec()
            if result == 0:
                newName = name.GetResult() or " "
                newProfileJSON = util.search(self.Profiles, current_item.text())
                print(newProfileJSON)
                self.Profiles[newName] = newProfileJSON.pop(current_item.text())
                print(self.Profiles)
                x = self.profilesList.insertItem(self.profilesList.row(current_item) + 1, newName)
        elif chosen_action == renameProfileAction:
            print("Rename")
            name = __Name__(self)
            result = name.exec()
            if result == 0:
                newName = name.GetResult() or " "
                self.Profiles[newName] = self.Profiles[current_item.text()]
                self.Profiles.pop(current_item.text())
                current_item.setText(newName)
        elif chosen_action == deleteProfileAction:
            print("Deleted")
            self.Profiles.pop(current_item.text())
            self.profilesList.takeItem(self.profilesList.row(current_item))
            self.profilesList.removeItemWidget(current_item)
        self.BindAll()
    
    def ManageProfilesFrame(self):
        layout = QGridLayout()
        self.profilesList = QListWidget()
        self.profilesList.addItems(list(util.search(self.Profiles, '*').keys()))
        self.profilesList.setDragDropMode(QAbstractItemView.InternalMove)
        self.profilesList.setDefaultDropAction(Qt.TargetMoveAction)
        self.profilesList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.profilesList.customContextMenuRequested.connect(self.ProfilesContextMenu)
        
        restartLabel = QLabel("You must save, close and re-open to display changes!")
        layout.addWidget(restartLabel,      1, 1, 1, 1)
        layout.addWidget(self.profilesList, 2, 1, 1, 1)
        
        return layout

    def ClickConfigFrame(self, profile):
        vertical = QVBoxLayout()
        for ConfigClass in util.values(self.Profiles, f'{profile}/ClickConfig')[0].keys():
            horizontal = QHBoxLayout()
            horizontal.addWidget(QLabel(ConfigClass))
            for ConfigOption in util.values(self.Profiles, f'{profile}/ClickConfig/{ConfigClass}')[0]:
                value = util.values(self.Profiles, f'{profile}/ClickConfig/{ConfigClass}/{ConfigOption}')[0]
                match ConfigOption:
                    case "Value":
                        widget = QLineEdit()
                        widget.setText(value)
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
        self.UnbindAll()
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
        self.BindAll()

        # PySide6.QtWidgets.QTabWidget.currentChanged(index)
        # PySide6.QtWidgets.QTabWidget.currentIndex()
        # PySide6.QtWidgets.QTabWidget.tabText(index)
        # keyboard.add_hotkey(v, lambda: toggle_autoclicker()

    def BindAll(self):
        self.UnbindAll()
        profile = self.tabs.tabText(self.tabs.currentIndex())
        for tabName in util.values(self.Profiles, f'{profile}/Keybinds')[0].keys():
            i = 0
            for group in util.values(self.Profiles, f'{profile}/Keybinds/{tabName}')[0].keys():
                i += 1
                for bind in util.values(self.Profiles, f'{profile}/Keybinds/{tabName}/{group}')[0]:
                    if bind:
                        print(bind)
                        keyboard.add_hotkey(bind, lambda: self.autoclicker.Toggle())

    def UnbindAll(self):
        keyboard.unhook_all()
    
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