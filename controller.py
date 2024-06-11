import time
import pygame
from enum import IntEnum

import game
import engine


class Window(IntEnum):
    GAME = 1
    SETTINGS = 2
    MAINMENU = 3


class Settings(IntEnum):
    ENGINE_COLOUR = 0
    ENGINE_DIFFICULTY = 1
    TIME_CONTROL = 2
    HIGHLIGHT_MOVES = 3
    AUTO_FLIP = 4
    PROM_TYPE = 5
    GRAB_MODE = 6


class Controller(game.DrawnObject):
    def __init__(self) -> None:
        super().__init__()

        self.active_window = Window.MAINMENU
        self.window_before_settings = Window.MAINMENU
        self.engine_mode = False
        self.quit_game = False

        self.x_offset = 0
        self.y_offset = 0

        self.settings_groups_names = {
            Settings.ENGINE_COLOUR: "Engine Plays As",
            Settings.ENGINE_DIFFICULTY: "Engine Difficulty",
            Settings.TIME_CONTROL: "Time Control",
            Settings.HIGHLIGHT_MOVES: "Highlight Last Move",
            Settings.AUTO_FLIP: "Auto Flip Board",
            Settings.PROM_TYPE: "Promotion Type",
            Settings.GRAB_MODE: "Grab Mode",
        }

        self.settings = {
            Settings.ENGINE_COLOUR: game.Setting([game.RadioButton("White", True), game.RadioButton("Black", False, True)]),
            Settings.ENGINE_DIFFICULTY: game.Setting(
                [game.RadioButton("Easy", "e"), game.RadioButton("Medium", "m", True), game.RadioButton("Hard", "h")]
            ),
            Settings.TIME_CONTROL: game.Setting([game.RadioButton("5 Min", 5), game.RadioButton("10 Min", 10, True), game.RadioButton("15 Min", 15)]),
            Settings.HIGHLIGHT_MOVES: game.Setting([game.RadioButton("Enabled", True, True), game.RadioButton("Disabled", False)]),
            Settings.AUTO_FLIP: game.Setting([game.RadioButton("Enabled", True), game.RadioButton("Disabled", False, True)]),
            Settings.PROM_TYPE: game.Setting([game.RadioButton("Auto Queen", True, True), game.RadioButton("Manually Choose", False)]),
            Settings.GRAB_MODE: game.Setting([game.RadioButton("Drag & Drop", True, True), game.RadioButton("Select Squares", False)]),
        }

        for i, setting in enumerate(self.settings.values()):
            setting.update_positions(i)

        self.update()

    def new_game(self) -> None:
        # sets variables for new game
        self.player_is_white = not self.settings[Settings.ENGINE_COLOUR].value()
        self.white_pov = self.player_is_white

        self.board = engine.Board()
        self.computer = engine.Engine()
        self.board_gui = game.Board()
        self.panel = game.Panel()

        self.held_piece = game.HeldPiece()
        self.next_moves = engine.move_gen(self.board)
        self.past_moves = [engine.BLANK_MOVE]

        time_min = self.settings[Settings.TIME_CONTROL].value()
        time_min = time_min if time_min is not None else 15
        self.wtime: float = time_min * 60
        self.btime: float = time_min * 60

        self.info_bar = "White to Move" if self.board.white_move else "Black to Move"

        self.w_last_time = time.time()
        self.b_last_time = time.time()

        self.game_over = False

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

        for i, setting in enumerate(self.settings.values()):
            setting.update_positions(i)

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

                    # check if we can grab piece (if it is the correct colour)
                    if piece.isalpha() and piece.isupper() == self.board.white_move:
                        self.held_piece.grab(pos, piece, self.next_moves)  # grab it

                    elif not self.settings[Settings.GRAB_MODE].value():
                        # otherwise check if in select square mode and see if we can drop our piece
                        move = self.get_move(x, y)
                        if move != engine.BLANK_MOVE:
                            self.make_move(move)

                        self.held_piece.drop()  # either way we drop the held piece

            else:
                # otherwise check for button presses
                if self.panel_buttons["flip"].is_over():
                    self.white_pov = not self.white_pov

                elif self.panel_buttons["home"].is_over():
                    self.active_window = Window.MAINMENU

                elif self.panel_buttons["settings"].is_over():
                    self.window_before_settings = self.active_window
                    self.active_window = Window.SETTINGS

                # if we are in select square  mode drop the held piece
                if not self.settings[Settings.GRAB_MODE].value():
                    self.held_piece.drop()

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
            for setting in self.settings.values():
                setting.handle_click()

            # check for back button
            if self.back_button.is_over():
                self.active_window = self.window_before_settings

    def mouse_release(self, x: int, y: int) -> None:
        if self.active_window == Window.GAME:
            # if in drag and drop mode
            if self.settings[Settings.GRAB_MODE].value():
                # determine the move played, if it wasn't blank then make the move
                move = self.get_move(x, y)
                if move != engine.BLANK_MOVE:
                    self.make_move(move)

                self.held_piece.drop()

    def get_move(self, x: int, y: int) -> engine.Move:
        if self.outside_board(x, y):
            return engine.BLANK_MOVE

        # get the rank and file
        rank = (y - self.y_padd) // self.unit
        file = (x - self.x_padd) // self.unit

        # if valid move
        dest = game.get_pos(rank, file, self.white_pov)

        for move in self.next_moves:
            if (self.held_piece.pos, dest) == (move.pos, move.dest):
                # set the promotion to queen since thats the one the player will want
                move.prom = "q" if move.prom else ""

                return move

        return engine.BLANK_MOVE

    def make_move(self, move: engine.Move) -> None:
        # make the move on the board and calculate new information
        self.board.make(move)
        self.past_moves.append(move)
        self.next_moves = engine.move_gen(self.board)

        # switch to the pov of player to move if auto-flip is on
        if self.settings[Settings.AUTO_FLIP].value():
            self.white_pov = self.board.white_move

        # reset last clock update times
        if self.board.white_move:
            self.w_last_time = time.time()
        else:
            self.b_last_time = time.time()

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

    def update_game(self, screen: pygame.surface.Surface) -> None:
        self.draw(screen)

        # if the game menu is active
        if self.active_window == Window.GAME:
            # if the game has not ended
            if not self.game_over:
                self.update_clocks()

                # if it is the computer's turn to move make a move
                if self.engine_mode and self.player_is_white != self.board.white_move:
                    move = self.computer.search(
                        self.board,
                        {"wtime": round(self.wtime * 1000), "btime": round(self.btime * 1000)},
                        difficulty=self.settings[Settings.ENGINE_DIFFICULTY].value(),
                    )

                    # since the move will be made without updating clocks we have to update here aswell
                    self.update_clocks()

                    if move is not engine.BLANK_MOVE:
                        self.make_move(move)

    def update_clocks(self) -> None:
        # update clock for the side to move
        if self.board.white_move:
            self.wtime -= time.time() - self.w_last_time
            self.w_last_time = time.time()
        else:
            self.btime -= time.time() - self.b_last_time
            self.b_last_time = time.time()

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.background_image, (0, 0))

        if self.active_window == Window.GAME:
            # draw the board
            self.board_gui.draw(
                screen,
                self.board,
                self.white_pov,
                self.held_piece,
                self.past_moves[-1],
                self.settings[Settings.HIGHLIGHT_MOVES].value(),
                self.settings[Settings.GRAB_MODE].value(),
                self.x_offset,
                self.y_offset,
            )

            # draw the side panel
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
            for setting in self.settings.values():
                for button in setting.buttons:
                    button.draw(screen, self.settings_button_font)

            # draw button categories label
            for group in self.settings:
                text = self.settings_title_font.render(self.settings_groups_names[group], True, game.WHITE)
                screen.blit(text, (self.x_padd, self.y_padd + self.unit * (2.5 + group) - text.get_height() // 2))

        pygame.display.flip()
