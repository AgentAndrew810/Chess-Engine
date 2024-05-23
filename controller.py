import time
import pygame

import game
import engine


class GameController(game.DrawnObject):
    def __init__(self) -> None:
        super().__init__()

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

        self.update()

        self.game_over = False
        self.player_is_white = True
        self.white_pov = True
        self.x_offset = 0
        self.y_offset = 0

    def update(self) -> None:
        button_height = self.y_padd + round(self.unit * 7.25)

        self.buttons = {
            "home": game.Button(self.x_padd + self.unit * 9, button_height, self.unit, round(self.unit * 0.75), "assets/home-icon.png"),
            "flip": game.Button(self.x_padd + self.unit * 10, button_height, self.unit, round(self.unit * 0.75), "assets/flip-icon.png"),
            "hint": game.Button(self.x_padd + self.unit * 11, button_height, self.unit, round(self.unit * 0.75), "assets/hint-icon.png"),
            "settings": game.Button(self.x_padd + self.unit * 12, button_height, self.unit, round(self.unit * 0.75), "assets/settings-icon.png"),
        }

        self.background_image = pygame.image.load("assets/background.png")
        self.background_image = pygame.transform.smoothscale(self.background_image, (self.screen_width, self.screen_height))

    @property
    def player_turn(self) -> bool:
        return self.player_is_white == self.board.white_move

    def outside_board(self, x: int, y: int) -> bool:
        if self.x_padd < x < self.x_padd + self.unit * 8:
            if self.y_padd < y < self.y_padd + self.unit * 8:
                return False

        return True

    def grab_piece(self, x: int, y: int) -> None:
        if self.outside_board(x, y):
            return

        # get the rank and file grabbed and their offsets
        rank, self.y_offset = divmod(y - self.y_padd, self.unit)
        file, self.x_offset = divmod(x - self.x_padd, self.unit)

        # get the pos and piece
        pos = game.get_pos(rank, file, self.white_pov)
        piece = self.board.board[pos]

        # check if grabbing the correct colour
        if piece.isalpha() and piece.isupper() == self.board.white_move:
            self.held_piece.grab(pos, piece, self.next_moves)

    def drop_piece(self, x: int, y: int) -> None:
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

    def make_computer_move(self) -> None:
        move = self.computer.search(self.board)
        self.update_clocks()

        if move is not engine.BLANK_MOVE:
            self.make_move(move)

    def make_move(self, move: engine.Move) -> None:
        # make the move on the board and calculate new information
        self.board.make(move)
        self.past_moves.append(move)
        self.next_moves = engine.move_gen(self.board)

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

    def update_clocks(self) -> None:
        if not self.game_over:
            if self.board.white_move:
                self.wtime -= time.time() - self.wstart
                self.wstart = time.time()
            else:
                self.btime -= time.time() - self.bstart
                self.bstart = time.time()

    def draw(self, screen: pygame.surface.Surface) -> None:
        # screen.blit(self.background_image, (0, 0))

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

        for button in self.buttons.values():
            button.draw(screen)
