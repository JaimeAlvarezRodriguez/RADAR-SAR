import tkinter

class SubMenu(tkinter.Menu):
    def __init__(self, name, master, options):
        super().__init__(tearoff=False)
        master.add_cascade(menu=self, label=name)
        for option in options:
            self.add_command(label=option[0], accelerator=option[1], command=option[2])

class Menu(tkinter.Menu):
    def __init__(self, menulist, guide):
        super().__init__(tearoff=False)
        self.menu = [SubMenu(sub_menu[0], self, sub_menu[1]) for sub_menu in menulist]
        m = tkinter.Menu()
        for i in range(4):
            m.add_cascade(label=guide[i][0], command=guide[i][1])
        self.menu[3].add_cascade(label="Ayuda", menu=m)