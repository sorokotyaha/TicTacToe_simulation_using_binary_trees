

from game_tree import GameSimulator as GS
from linked_binary_tree import LinkedBinaryTree
from board import Board


def main():
    gs = GS()
    print("To terminate game, type -1 -1")
    usrstep = gs.getUserStep()

    while usrstep[0] != -1:

        gs.make_step(gs.board(), usrstep[0], usrstep[1], Board.CROSS_CELL)

        if gs.board().check_for_win_combos(Board.CROSS_CELL):
            print(gs.board())
            print("CONGRATULATIONS! YOU WON!")
            break
        elif gs.board().is_full():
            print("TIGHT!")

        # generate two possible steps
        option1 = gs.generate_step(gs.board())
        option2 = gs.generate_step(gs.board())

        cross = gs.board().get_cross_cells()
        zeros = gs.board().get_zero_cells()

        # build two new boards
        board1 = Board(3, 3)
        board1.configure(cross.append(option1))
        board1.configure(zeros)

        board2 = Board(3, 3)
        board2.configure(cross[:-1].append(option2))
        board2.configure(zeros)

        # build two new decision binary trees
        tree1 = LinkedBinaryTree(board1)
        tree2 = LinkedBinaryTree(board2)

        # calculate the number of victories for each tree
        gs.fill_board(tree1, tree1)
        result1 = gs.get_numVictories()

        gs.clear_victories()

        gs.fill_board(tree2, tree2)
        result2 = gs.get_numVictories()

        # choose the step with the biggest number of victories
        if result1 > result2:
            gs.make_step(gs.board(), option1[0], option1[1], Board.ZERO_CELL)
        else:
            gs.make_step(gs.board(), option2[0], option2[1], Board.ZERO_CELL)

        print(gs.board())
        if gs.board().check_for_win_combos():
            print("YOU LOST!")
            break
        elif gs.board().check_for_win_combos(Board.CROSS_CELL):
            print("CONGRATULATIONS! YOU WON!")
            break
        print("To terminate game, type -1 -1")
        usrstep = gs.getUserStep()

if __name__ == '__main__':
    main()