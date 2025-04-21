import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1920x1080")
        self.title("Teleturniej")
        # self.configure(fg_color=BGCOL)

        self.columnconfigure((0, 2), weight=1, uniform='a')
        self.columnconfigure(1, weight=4)
        self.rowconfigure(0, weight=2, uniform='a')

        # Wigets
        self.teamsA = teamView(self)
        self.teamsA.grid(row=0, column=0, sticky='nswe')

        self.teamsB = teamView(self)
        self.teamsB.grid(row=0, column=2, sticky='nswe')

        # Maingame
        self.gameScreen = mainGame(self)
        self.gameScreen .grid(row=0, column=1, sticky='nswe')

        self.mainloop()


class teamView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init()
        self.configure(fg_color = "blue")


class mainGame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init()


if __name__ == '__main__':
    App()
