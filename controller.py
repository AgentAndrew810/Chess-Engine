import time
import pygame
from enum import Enum

import game
import engine


class Window(Enum):
    GAME = 1
    SETTINGS = 2
    MAINMENU = 3


class Controller(game.DrawnObject):
    def __init__(self) -> None:
        super().__init__()

        self.active_window = Window.MAINMENU
        self.window_before_settings = Window.MAINMENU
        self.game_over = False
        self.engine_mode = False
        self.quit_game = False

        self.x_offset = 0
        self.y_offset = 0

        # categories and their radio buttons
        self.setting_groups = {
            "Engine Plays As": ["White", "Black"],
            "Engine Difficulty": ["Easy", "Medium", "Hard"],
            "Time Control": ["5 Min", "10 Min", "15 Min"],
            "Highlight Last Move": ["Enabled", "Disabled"],
            "Auto Flip Board": ["Enabled", "Disabled"],
            "Promotion Type": ["Auto Queen", "Manually choose"],
            "Grab Mode": ["Drag & Drop", "Select squares"],
        }

        # temp positions for buttons
        x = self.x_padd + self.unit * 6
        y = self.y_padd + round(self.unit * 2.5)
        radius = self.unit // 4

        # add settings buttons
        self.settings = {}
        for i, category in enumerate(self.setting_groups):
            self.settings[category] = {}
            for j, button in enumerate(self.setting_groups[category]):
                self.settings[category][button] = game.RadioButton((x + self.unit * 3 * j, y + self.unit * i), radius, button, j == 0)

        self.update()

    def new_game(self) -> None:
        # sets variables for new game
        self.player_is_white = True
        self.white_pov = self.player_is_white

        self.board = engine.Board()
        self.computer = engine.Engine()

        self.board_gui = game.Board()
        self.panel = game.Panel()

        self.held_piece = game.HeldPiece()
        self.next_moves = engine.move_gen(self.board)
        self.past_moves = [engine.BLANK_MOVE]

        self.wtime: float = 15 * 60  # 15 minutes
        self.btime: float = 15 * 60

        self.info_bar = "White to Move" if self.board.white_move else "Black to Move"

        self.wstart = time.time()
        self.bstart = time.time()

    def update(self) -> None:
        # determine position and sizes of menu buttons
        x = self.x_padd + self.unit * 4
        y = self.y_padd + self.unit * 3
        width = self.unit * 6
        height = self.unit

        # all of the menu screen buttons
        self.menu_buttons = {
            "play-engine": game.MenuButton(x, y, width, height, "Play Engine", game.BLUE),
            "play-friend": game.MenuButton(x, y + round(self.unit * 1.25), width, height, "Play Friend", game.BLUE),
            "settings": game.MenuButton(x, y + round(self.unit * 2.5), width, height, "Settings", game.BLUE),
            "quit": game.MenuButton(x, y + round(self.unit * 3.75), width, height, "Quit", game.BLUE),
        }

        # determine position and sizes of game buttons (specifically on the panel)
        x = self.x_padd + self.unit * 9
        y = self.y_padd + round(self.unit * 7.25)
        height = round(self.unit * 0.75)
        width = round(self.unit * 5 / 4)

        # all of the buttons on the panel
        self.panel_buttons = {
            "home": game.Button(x, y, width, height, "assets/home-icon.png"),
            "flip": game.Button(x + width, y, width, height, "assets/flip-icon.png"),
            "hint": game.Button(x + width * 2, y, width, height, "assets/hint-icon.png"),
            "settings": game.Button(x + width * 3, y, width, height, "assets/settings-icon.png"),
        }

        # determine position and sizes of settings buttons
        x = self.x_padd + self.unit * 6
        y = self.y_padd + round(self.unit * 2.5)
        radius = self.unit // 4

        # resize settings buttons
        for i, category in enumerate(self.setting_groups):
            for j, button in enumerate(self.setting_groups[category]):
                self.settings[category][button].resize((x + self.unit * 3 * j, y + self.unit * i), radius)

        # back button
        self.back_button = game.Button(self.unit // 10, self.unit // 10, self.unit, self.unit, "assets/back-icon.png")

        # load the background image
        self.background_image = pygame.image.load("assets/background.png")
        self.background_image = pygame.transform.smoothscale(self.background_image, (self.screen_width, self.screen_height))

        # load all the fonts
        self.title_font = pygame.font.Font("assets/hercules.ttf", self.unit * 2)
        self.options_title_font = pygame.font.Font("assets/hercules.ttf", round(self.unit * 1.5))
        self.version_font = pygame.font.Font("assets/Inter.ttf", round(self.unit / 3))
        self.menu_button_font = pygame.font.Font("assets/Inter.ttf", round(self.unit / 2))
        self.settings_button_font = pygame.font.Font("assets/Inter.ttf", round(self.unit / 3))
        self.settings_title_font = pygame.font.Font("assets/Inter.ttf", round(self.unit / 2.25))

    @property
    def player_turn(self) -> bool:
        return self.player_is_white == self.board.white_move

    def outside_board(self, x: int, y: int) -> bool:
        if self.x_padd < x < self.x_padd + self.unit * 8:
            if self.y_padd < y < self.y_padd + self.unit * 8:
                return False

        return True

    def mouse_click(self, x: int, y: int) -> None:
        if self.active_window == Window.GAME:
            # if the grab is inside the board
            if not self.outside_board(x, y):
                # if it is the players turn to move
                if not self.engine_mode or self.player_is_white == self.board.white_move:
                    # get the rank and file grabbed and their offsets
                    rank, self.y_offset = divmod(y - self.y_padd, self.unit)
                    file, self.x_offset = divmod(x - self.x_padd, self.unit)

                    # get the pos and piece
                    pos = game.get_pos(rank, file, self.white_pov)
                    piece = self.board.board[pos]

                    # check if grabbing the correct colour
                    if piece.isalpha() and piece.isupper() == self.board.white_move:
                        self.held_piece.grab(pos, piece, self.next_moves)
            else:
                # otherwise check for button presses
                if self.panel_buttons["flip"].is_over():
                    self.white_pov = not self.white_pov

                elif self.panel_buttons["home"].is_over():
                    self.active_window = Window.MAINMENU

                elif self.panel_buttons["settings"].is_over():
                    self.window_before_settings = self.active_window
                    self.active_window = Window.SETTINGS

        elif self.active_window == Window.MAINMENU:
            # check for button presses
            if self.menu_buttons["play-engine"].is_over():
                self.active_window = Window.GAME
                self.engine_mode = True
                self.new_game()

            elif self.menu_buttons["play-friend"].is_over():
                self.active_window = Window.GAME
                self.engine_mode = False
                self.new_game()

            elif self.menu_buttons["settings"].is_over():
                self.window_before_settings = self.active_window
                self.active_window = Window.SETTINGS

            elif self.menu_buttons["quit"].is_over():
                self.quit_game = True

        elif self.active_window == Window.SETTINGS:
            # check for button presses
            for button_category in self.settings.values():
                for button in button_category.values():
                    if button.is_over():
                        # disable every other button in category
                        for button2 in button_category.values():
                            button2.enabled = False
                        # enable button
                        button.enabled = True
                        break

            # check for back button
            if self.back_button.is_over():
                self.active_window = self.window_before_settings

    def mouse_release(self, x: int, y: int) -> None:
        if self.active_window == Window.GAME:
            if self.outside_board(x, y):
                return

            # get the rank and file
            rank = (y - self.y_padd) // self.unit
            file = (x - self.x_padd) // self.unit

            # if valid move
            dest = game.get_pos(rank, file, self.white_pov)

            for move in self.next_moves:
                if (self.held_piece.pos, dest) == (move.pos, move.dest):
                    # set the promotion to queen since thats the one the player will want
                    move.prom = "q" if move.prom else ""

                    self.make_move(move)

                    # this is to make sure other moves aren't run (since there are 4 promotions)
                    break

            self.held_piece.drop()

    def make_move(self, move: engine.Move) -> None:
        # make the move on the board and calculate new information
        self.board.make(move)
        self.past_moves.append(move)
        self.next_moves = engine.move_gen(self.board)

        # switch to the pov of player to move if in friend mode
        if not self.engine_mode:
            self.white_pov = self.board.white_move

        # reset last clock update times
        if self.board.white_move:
            self.wstart = time.time()
        else:
            self.bstart = time.time()

        # update side to move in info bar
        if self.board.white_move:
            self.info_bar = "White to Move"
        else:
            self.info_bar = "Black to Move"

        # determine if the game is over
        if len(self.next_moves) == 0:
            if self.board.white_move:
                self.info_bar = "Black won by Checkmate!"
            else:
                self.info_bar = "White won by Checkmate!"

            self.game_over = True

        elif self.board.zobrist_key_history.count(self.board.hash) >= 2:
            self.info_bar = "Draw by repetition!"
            self.game_over = True

    def update_game(self) -> None:
        # if the game menu is active
        if self.active_window == Window.GAME:
            # if the game has not ended
            if not self.game_over:
                self.update_clocks()

                # if it is the computer's turn to move make a move
                if self.engine_mode and self.player_is_white != self.board.white_move:
                    move = self.computer.search(self.board)

                    # since the move will be made without updating clocks we have to update here aswell
                    self.update_clocks()

                    if move is not engine.BLANK_MOVE:
                        self.make_move(move)

    def update_clocks(self) -> None:
        # update clock for the side to move
        if self.board.white_move:
            self.wtime -= time.time() - self.wstart
            self.wstart = time.time()
        else:
            self.btime -= time.time() - self.bstart
            self.bstart = time.time()

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.background_image, (0, 0))

        if self.active_window == Window.GAME:
            self.board_gui.draw(
                screen,
                self.board,
                self.white_pov,
                self.held_piece,
                self.past_moves[-1],
                self.x_offset,
                self.y_offset,
            )

            self.panel.draw(screen, self.wtime, self.btime, self.info_bar)

            # draw buttons
            for button in self.panel_buttons.values():
                button.draw(screen)
        elif self.active_window == Window.MAINMENU:
            # draw title
            title_text = self.title_font.render("Chess Club 7", True, game.BLUE)
            title_rect = title_text.get_rect(center=(self.x_padd + self.unit * 7, self.y_padd + self.unit // 2))
            screen.blit(title_text, title_rect)

            # draw version
            version_text = self.version_font.render(f"v.{engine.VERSION}", True, game.LIGHT_GREY)
            version_rect = version_text.get_rect(
                center=(self.screen_width - version_text.get_width(), self.screen_height - version_text.get_height())
            )
            screen.blit(version_text, version_rect)

            # draw buttons
            for button in self.menu_buttons.values():
                button.draw(screen, self.menu_button_font)

        elif self.active_window == Window.SETTINGS:
            # draw options title
            title_text = self.options_title_font.render("Game Options", True, game.BLUE)
            title_rect = title_text.get_rect(center=(self.x_padd + self.unit * 7, self.y_padd))
            screen.blit(title_text, title_rect)

            # draw back button
            self.back_button.draw(screen)

            # draw buttons
            for button_category in self.settings.values():
                for button in button_category.values():
                    button.draw(screen, self.settings_button_font)

            # draw button categories
            for i, button_category in enumerate(self.setting_groups):
                text = self.settings_title_font.render(button_category, True, game.WHITE)
                screen.blit(text, (self.x_padd, self.y_padd + self.unit * (2.5 + i) - text.get_height() // 2))
