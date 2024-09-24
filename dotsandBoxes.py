from tkinter import *
from tkinter import font
import tkinter as tk
import random

TOL = 8
CELLSIZE = 60
OFFSET = 10
CIRCLERAD = 3
DOTOFFSET = OFFSET + CIRCLERAD
GAME_H = 600
GAME_W = 600
HORIZONTAL = "horizontal"
VERTICAL = "vertical"


class GameMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Dots and Boxes")
        self.root.geometry("600x500") #400x300

        self.login_label = tk.Label(root, text="صفحه ورود")
        self.login_label.pack(pady=30)
        self.login_label = tk.Label(root, text="نام کاربری:")
        self.login_label.pack()

        self.login_entry_player1 = tk.Entry(root)
        self.login_entry_player1.pack()

        self.password_label_player1 = tk.Label(root, text="رمز عبور:")
        self.password_label_player1.pack()

        self.password_entry_player1 = tk.Entry(root, show="*")
        self.password_entry_player1.pack()

        self.login_label = tk.Label(root, text="مشخصات بازیکن ۲")
        self.login_label.pack(pady=30)

        self.login_label2 = tk.Label(root, text=" نام کاربری:")
        self.login_label2.pack()

        self.login_entry_player2 = tk.Entry(root)
        self.login_entry_player2.pack()

        self.password_label_player2 = tk.Label(root, text="رمز عبور:")
        self.password_label_player2.pack()

        self.password_entry_player2 = tk.Entry(root, show="*")
        self.password_entry_player2.pack()

        self.login_button = tk.Button(root, text="ورود", command=self.login)
        self.login_button.pack()

        self.signup_button = tk.Button(root, text="ثبت نام", command=self.signup)
        self.signup_button.pack()

        

    def login(self):
        username_player1 = self.login_entry_player1.get()
        password_player1 = self.password_entry_player1.get()
        username_player2 = self.login_entry_player2.get()
        password_player2 = self.password_entry_player2.get()
        self.show_color_choices(username_player1, username_player2)

    def signup(self):
        username_player1 = self.login_entry_player1.get()
        password_player1 = self.password_entry_player1.get()
        username_player2 = self.login_entry_player2.get()
        password_player2 = self.password_entry_player2.get()
        self.show_color_choices(username_player1, username_player2)

    def show_color_choices(self, username_player1, username_player2):
        self.root.destroy() 
        color_menu = ColorMenu(username_player1, username_player2)

class ColorMenu:
    def __init__(self, username1, username2):
        self.root = tk.Tk()
        self.root.title("انتخاب رنگ")
        self.root.geometry("600x500")
        self.username1 = username1
        self.username2 = username2

        self.color_label1 = tk.Label(self.root, text=f"لطفا یک رنگ انتخاب کنید:{self.username1}")
        self.color_label1.pack() 

        colors1 = ["red", "blue", "green", "yellow", "black"]
        self.color_var1 = tk.StringVar(self.root)
        self.color_var1.set(colors1[0])

        self.color_menu1 = tk.OptionMenu(self.root, self.color_var1, *colors1)
        self.color_menu1.pack()

        self.space_label = tk.Label(self.root, text="-----------")
        self.space_label.pack(pady=30)

        self.color_label2 = tk.Label(self.root, text=f"لطفا یک رنگ انتخاب کنید:{self.username2}")
        self.color_label2.pack()

        colors2 = ["red", "blue", "green", "yellow", "black"]
        self.color_var2 = tk.StringVar(self.root)
        self.color_var2.set(colors2[1])

        self.color_menu2 = tk.OptionMenu(self.root, self.color_var2, *colors2)
        self.color_menu2.pack()

        self.play_button = tk.Button(self.root, text="شروع بازی", command=self.start_game)
        self.play_button.pack()

    def start_game(self):
        selected_color1 = self.color_var1.get()
        selected_color2 = self.color_var2.get()
        self.root.destroy()

        mainw = Tk()
        mainw.title('Dots and Boxes')
        mainw.f = MyFrame(mainw , self.username1, self.username2 ,selected_color1 ,selected_color2)
        mainw.mainloop()


class Player(object):

    def __init__(self, name, color="black"):
        self.score = 0
        self.str = StringVar()
        self.name = name
        self.color = color

    def update(self):
        self.str.set(self.name + ":  %d" % self.score)

class MyFrame(Frame):

    def __init__(self, master ,username1 ,username2 ,selected_color1 ,selected_color2):
        Frame.__init__(self, master)
        self.GO_font = font.Font(self.master, name="GOFont",
                    family="Times", weight="bold", size=36)
        self.canvas = Canvas(self, height=GAME_H, width=GAME_W)
        self.canvas.bind("<Button-1>", lambda e: self.click(e))
        self.canvas.grid(row=0, column=0)
        self.username1 = username1
        self.username2 = username2
        self.selected_color1 = selected_color1
        self.selected_color2 = selected_color2

        self.dots = [[self.canvas.create_oval(CELLSIZE * i + OFFSET, \
                                              CELLSIZE * j + OFFSET, \
                                              CELLSIZE * i + OFFSET + 2 * CIRCLERAD, \
                                              CELLSIZE * j + OFFSET + 2 * CIRCLERAD, \
                                              fill="green") \
                      for j in range(8)] for i in range(8)]
        self.lines = []

        self.infoframe = Frame(self)
        self.players = [Player(self.username1 , selected_color1 ), Player(self.username2, selected_color2)]
        self.infoframe.players = [Label(self.infoframe,
                                        textvariable=i.str) for i in self.players]
        for i in self.infoframe.players:
            i.grid()
        player_choice = random.choice([0,1])
        print(f"random choice player number {player_choice}")
        
        self.current_player_label = Label(self.infoframe, text=" نوبت  : ", background= "red")
        self.current_player_label.grid(row=len(self.players), column=0, columnspan=2)

        self.turn = self.players[player_choice]
        self.update_players()
        self.infoframe.grid(row=0, column=1, sticky=N)

        self.grid()

    def update_players(self):
        for i in self.players:
            i.update()

        self.current_player_label.config(text=" نوبت  : " + self.turn.name , background= self.turn.color)

    def click(self, event):
        x, y = event.x, event.y
        orient = self.isclose(x, y)

        if orient:
            if self.line_exists(x, y, orient):
                return
            l = self.create_line(x, y, orient)
            score = self.new_box_made(l)
            if score:
                self.turn.score += score
                self.turn.update()
                self.check_game_over()
            else:
                index = self.players.index(self.turn)
                self.turn = self.players[1 - index]
            self.lines.append(l)

        self.update_players()

    def create_line(self, x, y, orient):
        startx = CELLSIZE * ((x - OFFSET) // CELLSIZE) + DOTOFFSET
        starty = CELLSIZE * ((y - OFFSET) // CELLSIZE) + DOTOFFSET
        tmpx = (x - OFFSET) // CELLSIZE
        tmpy = (y - OFFSET) // CELLSIZE

        if orient == HORIZONTAL:
            endx = startx + CELLSIZE
            endy = starty
        else:
            endx = startx
            endy = starty + CELLSIZE
        line = self.canvas.create_line(startx, starty, endx, endy, fill=self.turn.color)
        return line

    def new_box_made(self, line):
        score = 0
        x0, y0, x1, y1 = self.canvas.coords(line)
        if x0 == x1: 
            midx = x0
            midy = (y0 + y1) / 2
            pre = (x0 - CELLSIZE / 2, midy)
            post = (x0 + CELLSIZE / 2, midy)
        elif y0 == y1:  
            midx = (x0 + x1) / 2
            midy = y0
            pre = (midx, y0 - CELLSIZE / 2)
            post = (midx, y0 + CELLSIZE / 2)

        if len(self.find_lines(pre)) == 3:
            self.fill_in(pre)  
            score += 1
        if len(self.find_lines(post)) == 3:
            self.fill_in(post)
            score += 1
        return score

    def find_lines(self, coords):
        x, y = coords
        if x < 0 or x > GAME_W:
            return []
        if y < 0 or y > GAME_W:
            return []
        
        lines = [x for x in self.canvas.find_enclosed(x - CELLSIZE, \
                                                      y - CELLSIZE, \
                                                      x + CELLSIZE, \
                                                      y + CELLSIZE) \
                 if x in self.lines]
        return lines

    def fill_in(self, coords):
        x, y = coords
        self.canvas.create_text(x, y, text=self.turn.name, fill=self.turn.color)

    def isclose(self, x, y):
        x -= OFFSET
        y -= OFFSET
        dx = x - (x // CELLSIZE) * CELLSIZE
        dy = y - (y // CELLSIZE) * CELLSIZE

        if abs(dx) < TOL:
            if abs(dy) < TOL:
                return None 
            else:
                return VERTICAL
        elif abs(dy) < TOL:
            return HORIZONTAL
        else:
            return None

    def line_exists(self, x, y, orient):
        id_ = self.canvas.find_closest(x, y, halo=TOL)[0]
        if id_ in self.lines:
            return True
        else:
            return False

    def check_game_over(self):
        total = sum([x.score for x in self.players])
        if total == 81:
            self.canvas.create_text(GAME_W / 2, GAME_H / 2, \
                                    text="GAME OVER", font="GOFont", \
                                    fill="#888")

if __name__ == "__main__":
    root = tk.Tk()
    game_menu = GameMenu(root)
    root.mainloop()
    
# DB password  score and score page