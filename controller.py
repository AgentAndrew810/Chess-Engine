import pygame
import time

import game
import engine


class GameController(game.DrawnObject):
    def __init__(self) -> None:
        super().__init__()

        x = self.x_padd + self.board_size + self.padd
        y = self.y_padd

        self.buttons = {
            "back": game.Button(x, y + self.square_size * 2, game.GREY),
            "flip": game.Button(x, y + self.square_size * 3, game.PURPLE),
            "quit": game.Button(x, y + self.square_size * 4, game.RED),
        }

        self.board = engine.Board()
        self.board_gui = game.Board()

        self.held_piece = game.HeldPiece()
        self.next_moves = engine.move_gen(self.board)
        self.last_move = engine.Move(-1, -1)

        self.player_is_white = True
        self.white_pov = self.player_is_white
        self.x_offset = 0
        self.y_offset = 0

    @property
    def player_turn(self) -> bool:
        return self.player_is_white == self.board.white_move

    def outside_board(self, x: int, y: int) -> bool:
        if not (self.x_padd < x < self.x_padd + self.board_size):
            return True
        elif not (self.y_padd < y < self.y_padd + self.board_size):
            return True

        return False

    def grab_piece(self, x: int, y: int) -> None:
        if self.outside_board(x, y):
            return

        # get the rank and file grabbed and their offsets
        rank, self.y_offset = divmod(y - self.y_padd, self.square_size)
        file, self.x_offset = divmod(x - self.x_padd, self.square_size)

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
        rank = (y - self.y_padd) // self.square_size
        file = (x - self.x_padd) // self.square_size

        # if valid move
        dest = game.get_pos(rank, file, self.white_pov)

        for move in self.next_moves:
            if (self.held_piece.pos, dest) == (move.pos, move.dest):
                # set the promotion to queen since thats the one the player will want
                if move.prom:
                    move.prom = "Q" if self.player_is_white else "q"

                # make the move
                self.board.make(move)
                self.last_move = move
                self.next_moves = engine.move_gen(self.board)

                # this is to make sure other moves aren't run (since there are 4 promotions)
                break

        self.held_piece.drop()

    def back(self) -> None:
        self.board.unmake(self.last_move)
        self.next_moves = engine.move_gen(self.board)

    def make_computer_move(self) -> None:
        start = time.time()
        move = engine.search(self.board)
        print(f"Time Taken: {round(time.time()-start, 3)}s")

        if move:
            self.board.make(move)
            self.last_move = move
        self.next_moves = engine.move_gen(self.board)

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill(game.BLACK)

        self.board_gui.draw(
            screen,
            self.board,
            self.white_pov,
            self.held_piece,
            self.last_move,
            self.x_offset,
            self.y_offset,
        )

        for button in self.buttons.values():
            button.draw(screen)
