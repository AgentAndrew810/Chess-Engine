import pygame

import game
import engine


class GameController(game.DrawnObject):
    def __init__(self) -> None:
        super().__init__()

        self.board = engine.Board()
        self.computer = engine.Engine()
        self.board_gui = game.Board()

        self.held_piece = game.HeldPiece()
        self.next_moves = engine.move_gen(self.board)
        self.last_move = engine.Move(-1, -1)

        self.game_over = False
        self.player_is_white = True
        self.white_pov = True
        self.x_offset = 0
        self.y_offset = 0

    @property
    def player_turn(self) -> bool:
        return self.player_is_white == self.board.white_move

    def outside_board(self, x: int, y: int) -> bool:
        if self.board_start_x < x < self.board_end_x:
            if self.board_start_y < y < self.y_padd + self.board_end_y:
                return False

        return True

    def grab_piece(self, x: int, y: int) -> None:
        if self.outside_board(x, y):
            return

        # get the rank and file grabbed and their offsets
        rank, self.y_offset = divmod(y - self.board_start_y, self.square_size)
        file, self.x_offset = divmod(x - self.board_start_x, self.square_size)

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
        rank = (y - self.board_start_y) // self.square_size
        file = (x - self.board_start_x) // self.square_size

        # if valid move
        dest = game.get_pos(rank, file, self.white_pov)

        for move in self.next_moves:
            if (self.held_piece.pos, dest) == (move.pos, move.dest):
                # set the promotion to queen since thats the one the player will want
                move.prom = "q" if move.prom else ""

                # make the move
                self.board.make(move)
                self.last_move = move
                self.next_moves = engine.move_gen(self.board)

                if self.board.zobrist_key_history.count(self.board.hash) >= 2:
                    print("Draw by 3 fold repetition!")
                    self.game_over = True

                # this is to make sure other moves aren't run (since there are 4 promotions)
                break

        self.held_piece.drop()

    def make_computer_move(self) -> None:
        move = self.computer.search(self.board)

        if move is not engine.BLANK_MOVE:
            self.board.make(move)
            self.last_move = move

            self.next_moves = engine.move_gen(self.board)

            if len(self.next_moves) == 0:
                print("Computer won by checkmate!")
                self.game_over = True

        else:
            print("Player won by checkmate!")
            self.game_over = True

        if self.board.zobrist_key_history.count(self.board.hash) >= 2:
            print("Draw by 3 fold repetition!")
            self.game_over = True

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
