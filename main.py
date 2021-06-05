import pygame
import sys
import random
import os
import resources
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Settings Klasse für die globalen Variablen.
class Settings:
    windowsize = 394
    height = 394
    width = 394
    grid = 17
    mines_max = 99
    grid_rows = 24
    grid_cols = 24
    win_condition = None
    mine_size = 32
    is_menu_used = False
    title = "Minesweeper - Grunwald"
    fps = 60
    pygame.font.init()
    font_size = 30
    font = pygame.font.SysFont("Helvetica", 30)
    file_path = os.path.dirname(os.path.abspath(__file__))
    images_path = os.path.join(file_path, "resources")

    def init_font():
        Settings.font_sizeont = pygame.font.SysFont("Helvetica", Settings.font_size)

    @staticmethod
    def get_dim():
        return Settings.windowsize, Settings.windowsize

    def change_diff(height, width, grid, mines_max, grid_rows, grid_cols, win_condition, mine_size, font_size):
        Settings.height = height
        Settings.width = width
        Settings.grid = grid
        Settings.mines_max = mines_max
        Settings.grid_rows = grid_rows
        Settings.grid_cols = grid_cols
        Settings.win_condition = win_condition
        Settings.mine_size = mine_size
        Settings.font_size = font_size
        Settings.font = pygame.font.SysFont("Helvetica", font_size)

# Klasse für das Spielfeld
class Area:
    def __init__(self, screen):
        self.grid_size = Settings.grid
        self.grid_rows = Settings.grid_rows
        self.grid_cols = Settings.grid_cols
        self.playable_area = []
        self.screen = screen
        self.win_counter = 0

    # Methode um eine Tilemap zu erstellen. Nach der erstellung der Tilemap werden mit self.spawn_mines() die Minen gesetzt.
    def build(self):
        for tile in range(self.grid_rows):
            self.playable_area.append(["-"]*Settings.grid_cols)

        self.spawn_mines()
        self.count_mines()

    # Diese Methode erstellt ein Gitter damit das placement der einzelnen Felder vereinfacht wird.
    def grid_builder(self, x, y):
        rect = pygame.Rect(0, 0, self.grid_size, self.grid_size)
        for i in range(0, (x // self.grid_size)+1): # Für jeden Gitterabschnitt der X-Achse wird ein Gitter auf der Y-Achse erstellt.
            for ii in range(0, (y // self.grid_size)+1):
                rect = pygame.Rect(i*self.grid_size, ii*self.grid_size, self.grid_size, self.grid_size)
        return rect

    # Mit dieser Methode werden die Minen auf das Spielfeld gesetzt.
    def spawn_mines(self):
        for mine in range(Settings.mines_max):
            mine_pos_x = random.randrange(Settings.grid, (Settings.width))
            mine_pos_y = random.randrange(Settings.grid, (Settings.height))
            temprary_grid = self.grid_builder(mine_pos_x, mine_pos_y)
            absolute_x = mine_pos_x//self.grid_size
            absolute_y = mine_pos_y//self.grid_size
            try:
                self.playable_area[absolute_x-1][absolute_y-1] = "x"
            except IndexError as ie:
                pass

    def count_mines(self):
        if Settings.mines_max != 99:
            self.mines_amount = 0
            for i in range(0, Settings.grid_cols):
                self.mines_amount += self.playable_area[i].count("x")
            if self.mines_amount != Settings.mines_max:
                self.playable_area = []
                self.build()

    # Hier werden die Minen aufgedeckt sobald der Spieler auf eine Mine drückt. Nach dem aufdecken wird das Spiel mit der Methode self.game_over() beendet.
    def show_mines(self, area, screen):
        for x in range(Settings.grid_rows):
            for y in range(Settings.grid_cols):
                if area[x][y] == "x":
                    r = pygame.Rect(x*self.grid_size, y*self.grid_size, self.grid_size, self.grid_size)
                    bomb = resources.BOMB_IMAGE[0]
                    bomb = pygame.transform.scale(bomb, (Settings.mine_size, Settings.mine_size))
                    screen.blit(bomb, r)
                    pygame.display.update()
                    pygame.time.wait(50)
        self.game_over()

    # Diese Methode wird verwendet um ein Overlay zurstellen das das gesamte Spielfeld bedeckt. Dies ist das Overlay das über die Felder gelegt wird.
    def area_overlay(self, screen):
        for x in range((Settings.width) // self.grid_size):
            for y in range((Settings.height) // self.grid_size):
                rect = pygame.Rect(x * self.grid_size, y * self.grid_size, self.grid_size, self.grid_size)
                pygame.draw.rect(screen, (109, 119, 155), rect, 0)
                pygame.draw.rect(screen, (78, 90, 133), rect, 5)
                pygame.draw.rect(screen, (185, 185, 185), rect, 1)

    # Bei der Methode wird ein TKinter Fenster geöffnet um eine Frage an den Spieler zu stellen. Hierbei hat der Spieler das Spiel verloren und er wird gefragt ob er noch eine Runde Spielen mag.
    def game_over(self):
        root = Tk().wm_withdraw()
        message = messagebox.askquestion("Verloren", "Möchtest du nochmal spielen?", icon='question')
        if message == 'yes':
            game = None
            game = Game()
            game.run()
        else:
            sys.exit()

    # Ist das selbe wie die Methode game_over()
    def win_window(self):
        root = Tk().wm_withdraw()
        message = messagebox.askquestion("Gewonnen!", "Möchtest du nochmal spielen?", icon='question')
        if message == 'yes':
            game = None
            game = Game()
            game.run()
        else:
            sys.exit()

    # Mit dieser Methode wird geprüft ob der Schritt der getätigt wird eine Bombe beinhaltet oder nicht. Ebenso wird die Methode benötigt um die Zahlen anzeigen zu lassen.
    def check_move(self, x, y, area):
        if x >= 0 and y >= 0:
            try:
                if area[x][y] == "x":
                    return True
            except IndexError:
                return False
            else:
                return False
        else:
            return False

    # Einfache Methode um Felder zu markieren.
    def mark(self, x, y, r):
        x = x // self.grid_size
        y = y // self.grid_size
        pygame.draw.rect(self.screen, (128,0,0), r)

    # Hier werden alle Schritte gescannt ob diese möglich sind oder zum Tod führen. Ebenso wird hier gecheckt ob eine Bombe in der nähe ist oder nicht.
    def move_scanning(self, x, y, r, color):
        x = x // self.grid_size
        y = y // self.grid_size
        self.count = 0
        if self.playable_area[x][y] == "x":
            print("Dead")
            self.show_mines(self.playable_area, self.screen)
        elif self.playable_area[x][y] != "x":
            if self.win_counter <= Settings.win_condition:
                if color != (255, 255, 255, 255):
                    if color != (0, 0, 0, 255):
                        self.win_counter += 1
            if self.win_counter == Settings.win_condition:
                self.win_window()
            if self.check_move(x, y-1, self.playable_area):
                self.count = self.count + 1
            if self.check_move(x, y+1, self.playable_area):
                self.count = self.count + 1
            if self.check_move(x+1, y, self.playable_area):
                self.count = self.count + 1
            if self.check_move(x-1, y, self.playable_area):
                self.count = self.count + 1
            if self.check_move(x-1, y-1, self.playable_area):
                self.count = self.count + 1
            if self.check_move(x+1, y+1, self.playable_area):
                self.count = self.count + 1
            if self.check_move(x-1, y+1, self.playable_area):
                self.count = self.count + 1
            if self.check_move(x+1, y-1, self.playable_area):
                self.count = self.count + 1
            
            pygame.draw.rect(self.screen, (255,255,255), r)

            if self.count == 0:
                pass
            else:
                n = Settings.font.render(str(self.count), True, (0,0,0))
                self.screen.blit(n, (r.x+10, r.y+4))

    # Dient zur Ausgabe des Spielfeldes in der Konsole.
    def debug(self):
        print(self.playable_area)

#Klasse für das Menü um die Schwierigkeit auszuwählen
class Menu:
    def __init__(self):
        self.app = Tk()
        self.app.geometry('300x100')
        self.app.title("Schwierigkeit")

        self.labelTop = Label(self.app, text='Wähle die Schwerigkeit aus.')
        self.labelTop.grid(column=0, row=0)
        self.comboExample = ttk.Combobox(self.app, values=["Einfach", "Mittel", "Schwer"])
        self.comboExample.grid(column=0, row=1)
        self.comboExample.bind("<<ComboboxSelected>>", self.recieve)
        self.comboExample.current()

        self.exit_button = Button(self.app, text="Ok", command=self.app.destroy)
        self.exit_button.grid(column=0, row=2)

        self.selection = None

    def recieve(self, event):
        self.selection = self.comboExample.get()

    def get_difficulty(self):
        return self.selection

    def run_menu(self):
        self.app.mainloop()

# Eigentliche Klasse für das Spiel. Hier werden die eigentliche Abläufe des Spiels durchgegangen.
class Game:
    def __init__(self):
        if Settings.is_menu_used == False:
            self.menu = Menu()
            self.menu.run_menu()
            Settings.is_menu_used = True

        try:
            if self.menu.get_difficulty() == 'Einfach':
                Settings.change_diff(397, 397, 44, 10, 9, 9, 71, 32, 30)
            if self.menu.get_difficulty() == 'Mittel':
                Settings.change_diff(400, 400, 25, 40, 16, 16, 216, 16, 15)
            if self.menu.get_difficulty() == 'Schwer':
                Settings.change_diff(275, 510, 17, 99, 30, 16, 381, 12, 10)
        except AttributeError:
            pass

        pygame.init()
        self.screen = pygame.display.set_mode((Settings.width, Settings.height))
        pygame.display.set_caption(Settings.title)
        self.done = False
        self.clock = pygame.time.Clock()
        #Settings.init_font()

        self.game_area = Area(self.screen)
        self.game_area.build()
        self.game_area.debug()
        self.limit = 0

    def run(self):
        while not self.done:
            self.clock.tick(Settings.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_x:
                        self.done = True
                    if event.key == pygame.K_l:
                        Settings.win_condition = 1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = pygame.mouse.get_pressed()
                    if state[0]:
                        x, y = pygame.mouse.get_pos()
                        color = self.screen.get_at((x, y))
                        temporary_rect = self.game_area.grid_builder(x, y)
                        self.game_area.move_scanning(x, y, temporary_rect, color)
                    if state[2]:
                        x, y = pygame.mouse.get_pos()
                        temporary_rect = self.game_area.grid_builder(x, y)
                        self.game_area.mark(x, y, temporary_rect)

            if self.limit == 0:
                self.game_area.area_overlay(self.screen)
                self.limit = 1
            
            
            pygame.display.update()

game = Game()
if __name__ == '__main__':
    game.run()
    #pygame.quit()