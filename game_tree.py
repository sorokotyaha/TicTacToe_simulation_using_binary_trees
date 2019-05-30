

from board import Board
from linked_binary_tree import LinkedBinaryTree
import random


class GameSimulator:
    """
    This class represents a tic tac toe game simulator, where
    computer plays with 0 and the player plays with X
    """
    MAXSTEPS = 9
    WON = 0
    LAST_PLAYER = None

    def __init__(self):
        """ Constructing GameSimulator"""
        self._board = Board(3, 3)
        self._mycell = 0

    def getUserStep(self):
        """
        This method gets the coordinates of the next step for player
        :return: list(int, int)
        """
        print("Type the row number and the column number of your next step:")
        line = input()
        return list(map(int, line.strip().split()))


    def board(self):
        """
        Returns the current state of a board
        :return: Board
        """
        return self._board

    def set_board(self, board):
        """
        Sets self._board to board
        :param board: Board
        """
        self._board = board

    @staticmethod
    def generate_step(board):
        """
        Generates a random step out of free. If there is no free cells,
        returns None
        :return: tuple
        """
        free = board.get_free_cells()
        if not free:
            return None
        step = random.choice(free)
        return step

    @staticmethod
    def make_step(board, row, col, value):
        """
        Sets the cell at row and col to a value
        :param row: int
        :param col: int
        :param value: int
        """
        if value == 0:
            board.set_zero_cell(row, col)
        else:
            board.set_cross_cell(row, col)
        GameSimulator.LAST_PLAYER = value

    def get_numVictories(self):
        """
        Returns the number of victories for the game simulation
        :return: float
        """
        return GameSimulator.WON / 2

    def clear_victories(self):
        """
        Sets number of victories to 0
        """
        GameSimulator.WON = 0

    def fill_board(self, board_node, tree):
        """
        This method takes a tree of boards and a node to work with.
        If the node contains a board with a winning combination of 0 or
        the board is full, returns tree. If there is still space left, generates
        two new steps out of available for the next player. Then creates two new
        Board objects and configures them with the new set of cross and zero cells.
        Then adds as children to board_node.
        :param board_node: LinkedBinaryTree
        :param tree: LinkedBinaryTree
        :return: LinkedBinaryTree
        """
        board = board_node.key

        cross = board.get_cross_cells()
        zeros = board.get_zero_cells()

        # check if board is full or 0 won
        if board.check_for_win_combos():
            GameSimulator.WON += 1
            return tree
        elif len(cross) + len(zeros) == GameSimulator.MAXSTEPS:
            return tree
        # if it's Cross turn
        elif len(cross) == len(zeros):
            GameSimulator.LAST_PLAYER = Board.CROSS_CELL
        # if it's Zeros turn
        else:
            GameSimulator.LAST_PLAYER = Board.ZERO_CELL

        fill_cell = GameSimulator.LAST_PLAYER
        # add child left
        step1 = self.generate_step(board)

        new_board1 = Board(3, 3)

        new_board1 = new_board1.configure(cross, Board.CROSS_CELL).configure(
            zeros, Board.ZERO_CELL)

        self.make_step(new_board1, step1[0], step1[1],
                       fill_cell)

        board_node.insert_left(new_board1)

        # add child right

        step2 = self.generate_step(new_board1)
        # if there was only 1 cell left for next step
        if not step2:
            step2 = step1

        new_board2 = Board(3, 3)
        new_board2.configure(cross, Board.CROSS_CELL)
        new_board2.configure(zeros, Board.ZERO_CELL)
        self.make_step(new_board2, step2[0], step2[1],
                       fill_cell)

        board_node.insert_right(new_board2)

        return self.fill_board(board_node.get_right_child(), tree), self.fill_board(
            board_node.get_left_child(), tree)


















