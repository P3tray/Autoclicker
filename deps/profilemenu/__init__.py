class Menu:
    def __init__(self, window, tk, ttk, callback):
        self.window = window
        self.tk = tk
        self.ttk = ttk
        self.callback = callback
        self.selected_profile = tk.StringVar()
    def createMenu(self, currentProfile, availableProfiles):
        if hasattr(self, 'ProfilesMenu'):
            self.ProfilesMenu.destroy()
            print("Destroyed")
        else:
            print("Not Destroyed")
        self.ProfilesMenu = self.ttk.OptionMenu(self.window, self.selected_profile, currentProfile, *availableProfiles, "New profile...", command = self.callback)
        self.ProfilesMenu.grid(row = 1, column = 1, columnspan = 2, pady = (0,0))
