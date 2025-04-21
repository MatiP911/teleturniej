import customtkinter as ctk

pallet = {
    "main":  "black",
    "second":  "blue",
    "third": "purple",
    "team": ("green", "blue"),
    "wrong": "red",
    "none": "grey",
    "bg": "black"
}

score = (0, 0)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1920x1080")
        self.title("Teleturniej")
        self.configure(fg_color=pallet['bg'])

        self.columnconfigure((0, 2), weight=1, uniform='a')
        self.columnconfigure(1, weight=4)
        self.rowconfigure(0, weight=2, uniform='a')

        # Wigets
        self.teamsA = teamView(self, 0)
        self.teamsA.grid(row=0, column=0, sticky='nswe')

        self.teamsB = teamView(self, 1)
        self.teamsB.grid(row=0, column=2, sticky='nswe')

        # Maingame
        self.gameScreen = mainGame(self)
        self.gameScreen .grid(row=0, column=1, sticky='nswe')

        self.mainloop()


class teamView(ctk.CTkFrame):
    def __init__(self, parent, teamNumber):
        super().__init__(parent)
        self.configure(fg_color="transparent")

        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=8, uniform='a')

        scoreViewer = ctk.CTkLabel(self, text_color=pallet['team'][teamNumber])
        scoreViewer.grid(row=0, column=0, sticky='nswe')


class mainGame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="transparent", border_width=40)


if __name__ == '__main__':
    App()
