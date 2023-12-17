import tkinter

class SubMenu(tkinter.Menu):
    def __init__(self, name, master, options):
        super().__init__(tearoff=False)
        master.add_cascade(menu=self, label=name)
        for option in options:
            self.add_command(label=option[0], accelerator=option[1], command=option[2])

class Menu(tkinter.Menu):
    def __init__(self, menulist = tuple):
        """
        Create a menu for the GUI

        Params
        ---
        menulist: tuple (("name", (("option", shortcut, callback), )), )

        """
        super().__init__(tearoff=False)
        self.menu = [SubMenu(sub_menu[0], self, sub_menu[1]) for sub_menu in menulist]