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
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=2, uniform='a')

        # create score
        self.scoreVar = (ctk.StringVar(value=""), ctk.StringVar(value=""))
        self.updateScoreView()

        # Wigets
        self.teamsA = teamView(self, 0)
        self.teamsA.grid(row=0, column=0, sticky='nswe')

        self.teamsB = teamView(self, 1)
        self.teamsB.grid(row=0, column=2, sticky='nswe')

        # Maingame
        self.gameScreen = mainGame(self)
        self.gameScreen .grid(row=0, column=1, sticky='nswe', padx=40, pady=40)

        self.mainloop()

    def updateScoreView(self):
        self.scoreVar[0].set(f"{score[0]}")
        self.scoreVar[1].set(f"{score[1]}")


class teamView(ctk.CTkFrame):
    def __init__(self, parent, teamNumber):
        super().__init__(parent)
        self.configure(fg_color="transparent")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=8)

        scoreViewer = ctk.CTkLabel(self, text_color=pallet['team'][teamNumber],
                                   textvariable=parent.scoreVar[teamNumber],
                                   font=('Tekton Pro', 40))
        scoreViewer.grid(row=0, column=0, sticky='nswe')


class mainGame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color='transparent')
        self.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')
        self.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        for i in range(5):
            for j in range(5):
                cell = Question(self, (i, j))
                cell.grid(row=i, column=j, sticky='nswe', padx=5, pady=5)


class Question(ctk.CTkFrame):
    def __init__(self, parent, id):
        super().__init__(parent)
        self.configure(border_width=5)


if __name__ == '__main__':
    App()
