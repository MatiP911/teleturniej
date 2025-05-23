import os
import customtkinter as ctk
from PIL import Image
from questions import questions

pallet = {
    "bg":  "#070304",
    "txt": "#F1F7ED",
    "team": ("#054F94", "#D62828", "#AC9F39"),
    "teamTxt": ("#F1F2EB", "#EAE2B7", "#1D1816"),
    "teamHover": ("#043F76", "#AC2020", "#998D33"),
    "none": "#464344",
    "noneHover": "#343233",
    'retake': 'red'
}


score = [0, 0]
retakeCount = [0, 3]

forLine = 100


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1920x1080")
        self.title("Teleturniej")
        self.configure(fg_color=pallet['bg'])

        # bgImg = Image.open("img/background.png")
        # bgImg = bgImg.resize((1920, 1080))
        # bgImgCtk = ctk.CTkImage(bgImg, size=(1920, 1080))
        # self.bgIMG = ctk.CTkLabel(self, image=bgImgCtk, text="")
        # self.bgIMG.place(x=0, y=0, relwidth=1, relheight=1)

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

        self.teamsA.lift()
        self.teamsB.lift()

        # Maingame
        self.gameScreen = mainGame(self)
        self.gameScreen .grid(row=0, column=1, sticky='nswe', padx=20, pady=80)

        self.gameScreen.lift()

        self.mainloop()

    def updateScoreView(self):
        self.scoreVar[0].set(f"{score[0]}")
        self.scoreVar[1].set(f"{score[1]}")


class teamView(ctk.CTkFrame):
    def __init__(self, parent, teamNumber):
        super().__init__(parent)
        self.parent = parent
        self.teamNumber = teamNumber
        self.configure(fg_color=pallet['bg'])

        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=1, uniform='a')
        self.rowconfigure(2, weight=8, uniform='a')

        scoreViewer = ctk.CTkLabel(self, text_color=pallet['team'][teamNumber],
                                   textvariable=parent.scoreVar[teamNumber],
                                   font=('Tekton Pro', 40),
                                   fg_color=pallet['bg'])
        scoreViewer.grid(row=0, column=0, sticky='nswe')
        scoreViewer.bind('<Button-1>', self.changeScore)

        retakeView = retakes(self, teamNumber)
        retakeView.grid(row=1, column=0, sticky='nswe')
        retakeView.bind('<Button-1>', retakeView.onRetakeLeftClick)
        retakeView.bind('<Button-3>', retakeView.onRetakeRightClick)

        teamMembersView = viewteamMembers(self, teamNumber)
        teamMembersView.grid(row=2, column=0, sticky='nswe')

    def changeScore(self, _):
        dialog = ctk.CTkInputDialog(text="Change score:", title="Change score")
        newScore = dialog.get_input()
        if newScore is None or newScore == '':
            return
        score[self.teamNumber] = int(newScore)
        self.parent.updateScoreView()


class viewteamMembers(ctk.CTkFrame):
    def __init__(self, parent, teamNumber):
        super().__init__(parent)

        self.configure(fg_color=pallet['bg'])

        self.load_images(teamNumber)

        self.columnconfigure(0, weight=1, uniform='a')
        for i in range(len(self.imgs)):
            self.rowconfigure(i, weight=1, uniform='a')

        for i, img in enumerate(self.imgs):
            label = ctk.CTkLabel(self, image=img, text="",
                                 fg_color=pallet['bg'])
            label.grid(row=i, column=0, pady=5)

    def load_images(self, teamNumber):
        temp = ('img/teams/teamA', 'img/teams/teamB')
        folder = temp[teamNumber]
        self.imgs = []
        for filename in os.listdir(folder):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                uri = os.path.join(folder, filename)
                img = Image.open(uri)
                img = img.resize((600, 600))
                ctkImg = ctk.CTkImage(
                    light_image=img, dark_image=img, size=(300, 300))
                self.imgs.append(ctkImg)
        return self.imgs


class retakes(ctk.CTkFrame):
    def __init__(self, parent, teamNumber):
        super().__init__(parent)
        self.teamNumber = teamNumber

        self.configure(fg_color=pallet['bg'])
        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')

        self.table = [0] * 5
        for i in range(5):
            self.table[i] = ctk.CTkLabel(
                self, text='[x]', text_color=pallet['retake'],
                font=('Adobe Arabic', 30))
            self.table[i].grid(row=0, column=i+1, sticky='nswe')
            self.table[i].bind('<Button-1>', self.onRetakeLeftClick)
            self.table[i].bind('<Button-3>', self.onRetakeRightClick)

        self.updateRetakes()

    def updateRetakes(self):
        for i in range(5):
            if i <= retakeCount[self.teamNumber]:
                self.table[i].configure(text='[X]')
            else:
                self.table[i].configure(text='')

    def onRetakeLeftClick(self, event):
        if retakeCount[self.teamNumber] >= 0:
            retakeCount[self.teamNumber] -= 1
            self.updateRetakes()

    def onRetakeRightClick(self, event):
        if retakeCount[self.teamNumber] < 5:
            retakeCount[self.teamNumber] += 1
            self.updateRetakes()


class mainGame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color='transparent')
        self.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')
        self.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        self.matrix = [[0 for _ in range(5)] for _ in range(5)]

        for i in range(5):
            for j in range(5):
                self.matrix[i][j] = Question(self, (j+5*i))
                self.matrix[i][j].grid(
                    row=i, column=j, sticky='nswe', padx=5, pady=5)

        self.matrix[2][2].configure(fg_color="#999999", text="Blank")
        self.matrix[2][2].team = 3

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
            self.checkLine(row, col)
        else:
            self.after(300, lambda: self.checkMatrix(row, col))

    def checkLine(self, row, col):
        team = self.matrix[row][col].team
        if team == -1:
            return

        # Pomocnicza funkcja do sprawdzania, czy komórka jest pasująca (dla TeamA, TeamB lub mydło)
        def same_or_soap(cell_team):
            return cell_team == team or cell_team == 3

        # Sprawdzenie kolumny
        if all(same_or_soap(self.matrix[i][col].team) for i in range(5)):
            score[team] += forLine
            self.parent.updateScoreView()

        # Sprawdzenie wiersza
        if all(same_or_soap(self.matrix[row][i].team) for i in range(5)):
            score[team] += forLine
            self.parent.updateScoreView()

        # Sprawdzenie przekątnej (lewa górna do prawa dolna)
        if all(same_or_soap(self.matrix[i][i].team) for i in range(5)):
            score[team] += forLine
            self.parent.updateScoreView()

        # Sprawdzenie przekątnej (prawa górna do lewa dolna)
        if all(same_or_soap(self.matrix[i][4 - i].team) for i in range(5)):
            score[team] += forLine
            self.parent.updateScoreView()


class Question(ctk.CTkButton):
    def __init__(self, parent, id):
        super().__init__(parent)
        self.parent = parent
        self.team = -1
        self.points = questions[id][0]
        self.configure(fg_color=pallet['none'], text=str(
            self.points), corner_radius=10, text_color=pallet['txt'],
            hover_color=pallet['noneHover'])
        self.configure(command=lambda: (
            setattr(self, 'team', -1), parent.guess(id)))

    def reconfigure(self):
        if self.team in [0, 1, 2]:
            if self.team != 2:
                score[self.team] += self.points
                self.parent.parent.updateScoreView()
            self.configure(fg_color=pallet['team'][self.team],
                           text_color=pallet['teamTxt'][self.team],
                           hover_color=pallet['teamHover'][self.team])


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

        questionNumer = ctk.CTkLabel(
            self, text=f"Pytanie {id}:", text_color=pallet['txt'])
        questionNumer.grid(row=0, column=0, columnspan=3, sticky='nswe')

        question = ImgTxtFrame(self, id)
        question.grid(row=1, column=0, columnspan=3, sticky='nswe')

        if id != 12:
            butTeamA = ctk.CTkButton(self, text='TeamA', font=('Tekton Pro', 20),
                                     command=lambda: self.buttonClicked(0),
                                     fg_color=pallet['team'][0],
                                     text_color=pallet['teamTxt'][0],
                                     hover_color=pallet['teamHover'][0])
            butTeamA.grid(row=2, column=0, sticky='nswe', padx=5, pady=10)

            butTeamN = ctk.CTkButton(self, text='Nikt', font=('Tekton Pro', 20),
                                     command=lambda: self.buttonClicked(2),
                                     fg_color=pallet['team'][2],
                                     text_color=pallet['teamTxt'][2],
                                     hover_color=pallet['teamHover'][2])
            butTeamN.grid(row=2, column=1, sticky='nswe', padx=5, pady=10)

            butTeamB = ctk.CTkButton(self, text='TeamB', font=('Tekton Pro', 20),
                                     command=lambda: self.buttonClicked(1),
                                     fg_color=pallet['team'][1],
                                     text_color=pallet['teamTxt'][1],
                                     hover_color=pallet['teamHover'][1])
            butTeamB.grid(row=2, column=2, sticky='nswe', padx=5, pady=10)

        else:
            self.after(1000, self.buttonClickedForSoap)  # np. auto zamkniecie po 3s


    def buttonClicked(self, teamID):
        row = self.id // 5
        col = self.id % 5
        self.parent.matrix[row][col].team = teamID
        self.destroy()

    def buttonClickedForSoap(self):
        row = self.id // 5
        col = self.id % 5
        self.parent.matrix[row][col].team = 3  # Neutralne mydło
        self.destroy()


class ImgTxtFrame(ctk.CTkFrame):
    def __init__(self, parent, id):
        super().__init__(parent)
        self.configure(fg_color=pallet['none'])

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        self.question = questions[id][1]
        self.answ = questions[id][2]

        self.ifQuestion = True
        self.load_another()

        print(id, self.answ)
        self.bind('<Button-1>', lambda event: self.load_another())

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

    def load_another(self):
        if self.ifQuestion:
            self.load_text(self.question)
        else:
            self.load_text(self.answ)
        self.ifQuestion = not self.ifQuestion

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
        self.txtLabel = ctk.CTkLabel(
            self, text=self.text, text_color=pallet['txt'])
        self.txtLabel.grid(row=0, column=0, padx=10, pady=10, sticky='nswe')
        self.txtLabel.bind('<Button-1>', lambda event: self.load_another())

        if self.imgLabel:
            self.imgLabel.grid(row=1, column=0, padx=10, pady=10)
            self.imgLabel.bind('<Button-1>', lambda event: self.load_another())


if __name__ == '__main__':
    App()
