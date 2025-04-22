import customtkinter as ctk
from PIL import Image

pallet = {
    "main":  "black",
    "txt": "white",
    "team": ("green", "blue", "red"),
    "teamTxt": ("blue", "green", "white"),
    "teamHover": ("red", "red", "blue"),
    "none": "grey",
    "bg": "black"
}


score = [0, 0]


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1920x1080")
        self.title("Teleturniej")
        self.configure(fg_color=pallet['bg'])

        self.columnconfigure((0, 2), weight=1, uniform='a')
        self.columnconfigure(1, weight=2, uniform='a')
        self.rowconfigure(0, weight=2, uniform='a')

        # Create score
        self.scoreVar = (ctk.StringVar(value=""), ctk.StringVar(value=""))
        self.updateScoreView()

        # Wigets
        self.teamsA = teamView(self, 0)
        self.teamsA.grid(row=0, column=0, sticky='nswe')

        self.teamsB = teamView(self, 1)
        self.teamsB.grid(row=0, column=2, sticky='nswe')

        # Maingame
        self.gameScreen = mainGame(self)
        self.gameScreen .grid(row=0, column=1, sticky='nswe', padx=20, pady=80)

        self.mainloop()

    def updateScoreView(self):
        self.scoreVar[0].set(f"{score[0]}")
        self.scoreVar[1].set(f"{score[1]}")


class teamView(ctk.CTkFrame):
    def __init__(self, parent, teamNumber):
        super().__init__(parent)
        self.configure(fg_color="transparent")

        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=8, uniform='a')

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

        self.matrix = [[0 for _ in range(5)] for _ in range(5)]

        for i in range(5):
            for j in range(5):
                self.matrix[i][j] = Question(self, (j+5*i))
                self.matrix[i][j].grid(
                    row=i, column=j, sticky='nswe', padx=5, pady=5)

    def guess(self, id):
        tempQuestionFrame = QuestionFrame(self, id)
        tempQuestionFrame.grid(row=0, column=0, rowspan=5,
                               columnspan=5, sticky='nswe')
        row = id // 5
        col = id % 5
        self.checkMatrix(row, col)

    def checkMatrix(self, row, col):
        if self.matrix[row][col].team != -1:
            self.matrix[row][col].reconfigure()
        else:
            self.after(300, lambda: self.checkMatrix(row, col))


class Question(ctk.CTkLabel):
    def __init__(self, parent, id):
        super().__init__(parent)
        self.team = -1
        self.configure(fg_color=pallet['none'], text=str(id), corner_radius=10)
        self.bind('<Button-1>', lambda event: parent.guess(id))

    def reconfigure(self):
        if self.team in [0, 1, 2]:
            self.configure(fg_color=pallet['team'][self.team],
                           text_color=pallet['team'][self.team])


class QuestionFrame(ctk.CTkFrame):
    def __init__(self, parent, id):
        super().__init__(parent)
        self.parent = parent
        self.id = id
        self.configure(fg_color=pallet['bg'])

        self.columnconfigure((0, 1, 2), weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=7, uniform='a')
        self.rowconfigure(2, weight=2, uniform='a')

        questionNumer = ctk.CTkLabel(self, text=f"Pytanie {id}:")
        questionNumer.grid(row=0, column=0, columnspan=3, sticky='nswe')

        question = ImgTxtFrame(self, id)
        question.grid(row=1, column=0, columnspan=3, sticky='nswe')

        butTeamA = ctk.CTkButton(self,
                                 command=lambda: self.buttonClicked(0),
                                 fg_color=pallet['team'][0],
                                 text_color=pallet['teamTxt'][0],
                                 hover_color=pallet['teamHover'][0])
        butTeamA.grid(row=2, column=0, sticky='nswe', padx=5, pady=10)

        butTeamN = ctk.CTkButton(self,
                                 command=lambda: self.buttonClicked(2),
                                 fg_color=pallet['team'][2],
                                 text_color=pallet['teamTxt'][2],
                                 hover_color=pallet['teamHover'][2])
        butTeamN.grid(row=2, column=1, sticky='nswe', padx=5, pady=10)

        butTeamB = ctk.CTkButton(self,
                                 command=lambda: self.buttonClicked(1),
                                 fg_color=pallet['team'][1],
                                 text_color=pallet['teamTxt'][1],
                                 hover_color=pallet['teamHover'][1])
        butTeamB.grid(row=2, column=2, sticky='nswe', padx=5, pady=10)

    def buttonClicked(self, teamID):
        row = self.id // 5
        col = self.id % 5
        self.parent.matrix[row][col].team = teamID
        self.destroy()


class ImgTxtFrame(ctk.CTkFrame):
    def __init__(self, parent, id):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        text = '[img/test.png](1000x300) aaaa'
        answ = 'test'
        self.load_text(text)

        self.bind('<Button-1>', lambda event: self.load_text(answ))

    def load_image(self, uri, width, height):
        try:
            img = Image.open(uri)

            img = img.resize((width, height))
            self.ctkImg = ctk.CTkImage(
                light_image=img, dark_image=img, size=(width, height))

            self.imgLabel = ctk.CTkLabel(self, image=self.ctkImg, text='')
        except Exception as e:
            print(f"Unable to load img: {e}")
            self.imgLabel = None

    def load_text(self, text):
        for widget in self.winfo_children():
            widget.destroy()

        self.text = text

        self.imgLabel = None
        width, height = 500, 500

        if text.startswith("[") and "]" in text:
            end_index = text.find(']')
            link = text[1:end_index]
            if text[end_index+1:].startswith('('):
                size_end = text.find(')', end_index)
                if size_end != -1:
                    size_str = text[end_index+2:size_end]
                    if 'x' in size_str:
                        w, h = size_str.split('x')
                        try:
                            width = int(w)
                            height = int(h)
                        except ValueError:
                            pass
                    self.text = text[size_end+1:].strip()
                else:
                    self.text = text[end_index+1:].strip()
            else:
                self.text = text[end_index+1:].strip()

            self.load_image(link, width, height)
        self.txtLabel = ctk.CTkLabel(self, text=self.text)
        self.txtLabel.grid(row=0, column=0, padx=10, pady=10, sticky='nswe')

        if self.imgLabel:
            self.imgLabel.grid(row=1, column=0, padx=10, pady=10)


if __name__ == '__main__':
    App()
