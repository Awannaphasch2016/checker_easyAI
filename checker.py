# !/usr/bin/env python3
from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax
from easyAI import solve_with_iterative_deepening
import numpy as np

# black_square
even = [0,2,4,6]
odd = [1,3,5,7]

even_row = [(i,j) for i in even for j in odd]
odd_row = [(i,j) for i in odd for j in even]

black_squares = even_row + odd_row

class Checker(TwoPlayerGame):

    def __init__(self, players):
        self.players = players
        # self.board = np.arange(8 * 8).reshape(8,8)
        self.blank_board = np.zeros((8,8), dtype=object)
        self.board = self.blank_board.copy()
        self.black_pieces = [
            (0,1), (0,3), (0,5), (0,7),
            (1,0), (1,2), (1,4), (1,6)
        ]
        self.white_pieces = [
            (6,1), (6,3), (6,5), (6,7),
            (7,0), (7,2), (7,4), (7,6)
        ]
        for i,j in self.black_pieces:
            self.board[i,j] = "B"
        for i,j in self.white_pieces:
            self.board[i,j] = "W"

        self.white_territory = [(7,0), (7,2), (7,4), (7,6)]
        self.black_territory = [(0,1), (0,3), (0,5), (0,7)]


        self.players[0].pos = self.white_pieces
        self.players[1].pos = self.black_pieces

        self.current_player = 1  # player 1 starts.

    def possible_moves_on_white_turn(self):

        table_pos = []
        old_new_piece_pos = []
        board = self.board
        # get legal move of each pieces. (old piece location, new piece location)
        # get position of each move (list of all table position)
        for v in self.players[self.current_player-1].pos:
            old_piece_pos = v

            step_pos = [(v[0]-1, v[1]-1), (v[0]-1, v[1]+1)]
            # if no piece at step_pos, step
            # otherwise jump until no piece at next step_pos
            for n in step_pos:
                if (n[0] >= 0 and n[0] <= 7) and (n[1] >= 0 and n[1] <= 7) and (n in black_squares):
                    if board[n[0], n[1]] in ["B","W"]:
                        y = ((n[0] - old_piece_pos[0]) * 2) + old_piece_pos[0]
                        x = ((n[1] - old_piece_pos[1]) * 2) + old_piece_pos[1]
                        j = (y,x)
                        is_inside_board = (j[0] >= 0 and j[0] <= 7) and (j[1] >= 0 and j[1] <= 7)
                        if (j[0] <= 7) and (j[1] <=7):
                            is_position_empty = (board[j[0], j[1]] == 0)
                        else:
                            is_position_empty = False
                        if is_inside_board and (j in black_squares) and is_position_empty:
                            # print(old_piece_pos,j)
                            old_new_piece_pos.append((old_piece_pos,j))
                    else:
                        old_new_piece_pos.append((old_piece_pos,n))

        # board position before move
        board = self.blank_board
        for (p,l) in zip(self.players, ["W", "B"]):
            for x,y in p.pos:
                board[x,y] = l

        # board position after  move
        for i,j in old_new_piece_pos:
            b = board.copy()
            b[i[0], i[1]] = 0
            b[j[0], j[1]] = "W"
            # print(b)
            table_pos.append(b)
        return table_pos

    def possible_moves_on_black_turn(self):
        table_pos = []
        old_new_piece_pos = []
        board = self.board
        # get legal move of each pieces. (old piece location, new piece location)
        # get position of each move (list of all table position)
        for v in self.players[self.current_player-1].pos:
            old_piece_pos = v

            step_pos = [(v[0]+1, v[1]-1), (v[0]+1, v[1]+1)]
            # if no piece at step_pos, step
            # otherwise jump until no piece at next step_pos
            for n in step_pos:
                if (n[0] >= 0 and n[0] <= 7) and (n[1] >= 0 and n[1] <= 7) and (n in black_squares):
                    if board[n[0], n[1]] in ["B","W"]:
                        y = ((n[0] - old_piece_pos[0]) * 2) + old_piece_pos[0]
                        x = ((n[1] - old_piece_pos[1]) * 2) + old_piece_pos[1]
                        j = (y,x)
                        is_inside_board = (j[0] >= 0 and j[0] <= 7) and (j[1] >= 0 and j[1] <= 7)
                        if (j[0] <= 7) and (j[1] <=7):
                            is_position_empty = (board[j[0], j[1]] == 0)
                        else:
                            is_position_empty = False
                        if is_inside_board and (j in black_squares) and is_position_empty:
                            # print(old_piece_pos,j)
                            old_new_piece_pos.append((old_piece_pos,j))
                    else:
                        old_new_piece_pos.append((old_piece_pos,n))

        # board position before move
        board = self.blank_board
        for (p,l) in zip(self.players, ["W", "B"]):
            for x,y in p.pos:
                board[x,y] = l
        print(f"board = \n{board}")

        # board position after  move

        for i,j in old_new_piece_pos:
            b = board.copy()
            b[i[0], i[1]] = 0
            b[j[0], j[1]] = "B"
            table_pos.append(b)
            assert len(np.where(b != 0)[0]) == 16, f"there are {len(np.where(b != 0)[0])} pieces on the board  \n {b}"

        return table_pos

    def possible_moves(self):
        """
        """

        if self.current_player == 2:
            return self.possible_moves_on_black_turn()
        else:
            return self.possible_moves_on_white_turn()

    def get_piece_pos_from_table(self, table_pos):
        x = np.where(table_pos == "W")
        return [(i,j) for i,j in zip(x[0], x[1])]

    def make_move(self, pos):
        # update board
        self.players[self.current_player-1].pos = self.get_piece_pos_from_table(pos)

    def lose(self):
        """
        """
        if self.current_player == 2: # black lose

            for i in self.black_territory:
                if self.board[i[0],i[1]] == "W":
                    return True
            return False

        else: # white lose
            for i in self.white_territory:
                if self.board[i[0],i[1]] == "B":
                    return True
            return False

    def is_over(self):
        """
        over when finish game = N-1, and current game just finish.
        """
        return self.lose()

    def show(self):
        """
        show 8*8 checker board.
        """

        # board position before move
        board = self.blank_board
        for (p,l) in zip(self.players, ["W", "B"]):
            for x,y in p.pos:
                board[x,y] = l
        print('\n')
        print(board)

    def scoring(self):
       """
       win = 0
       lose = -100
       """
       return -100 if self.lose() else 0

if __name__ == "__main__":
    ai = Negamax(1) # The AI will think 13 moves in advance
    game = Checker( [ AI_Player(ai), AI_Player(ai) ] )
    history = game.play()
