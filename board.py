import random
import copy
# from linked_binary_tree import LinkedBinaryTree
from btree import LinkedBinaryTree


class Board:
    """Represents Board"""

    # constants - using Oles'
    NOUGHT = -1
    CROSS = 1
    EMPTY = 0

    CROSS_WON = 1
    NOUGHT_WON = -1
    CONTINUE = 2
    FINISH = 0
    

    def __init__(self):
        self.board = [[0] * 3 for i in range(3)]
        self.last_move = Board.NOUGHT
        self.number_of_moves = 0

    def check_results(self):
        """Checks current situatoin on board"""
        results = {3: Board.CROSS_WON, -3: Board.NOUGHT_WON}
        for row in self.board:
            summ = sum(row)
            if summ in results:
                return results[summ]
        for i in range(3):
            summ = self.board[0][i] + self.board[1][i] + self.board[2][i]
            if summ in results:
                return results[summ]
        summ = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if summ in results:
                return results[summ]
        summ = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if summ in results:
                return results[summ]
        if self.number_of_moves == 9:
            return Board.FINISH
        return Board.CONTINUE

    def make_move(self, cell):
        """Make move for player"""
        assert self.board[cell[0]][cell[1]] == Board.EMPTY, 'Error: not empty cell'
        assert cell[0] in (0, 1, 2) and cell[1] in (0, 1, 2),\
        'Error: coordinates out of range'
        self.last_move = -self.last_move
        self.board[cell[0]][cell[1]] = self.last_move
        self.number_of_moves += 1
        

    def random_move(self):
        """Make random move for generating tree"""
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == Board.EMPTY:
                    moves.append((i, j))
        cell = random.choice(moves)
        self.last_move = -self.last_move
        self.board[cell[0]][cell[1]] = self.last_move
        self.number_of_moves += 1

    def computer_move(self):
        """Make computer move: 
        generates binary tree and determines the best move"""
        board = copy.deepcopy(self)
        tree = LinkedBinaryTree(board)
        
        def recurse(root):
            """Build tree recursion
            :param root: current root
            :return: tuple with leaves"""
            if root.data.check_results() != Board.CONTINUE:
                return root.data.check_results()
            board_left = copy.deepcopy(root.data)
            board_right = copy.deepcopy(root.data)
            board_left.random_move()
            board_right.random_move()
            root.left = LinkedBinaryTree(board_left)
            root.right = LinkedBinaryTree(board_right)
            return recurse(root.left), recurse(root.right)

        leaves = recurse(tree)
        ######################
        left_results, right_results = [], []

        def search_from_tuple(leaves, results):
            """Take leaves from tuples"""
            if not isinstance(leaves, tuple):
                results.append(leaves)
            else:
                for leaf in leaves:
                    search_from_tuple(leaf, results)
        
        search_from_tuple(leaves[0], left_results)
        search_from_tuple(leaves[1], right_results)
        ######################
        self.last_move = -self.last_move
        left_count = left_results.count(self.last_move)
        right_count = right_results.count(self.last_move)
        if left_count < right_count:
            return copy.deepcopy(tree.right.data)
        else:
            return copy.deepcopy(tree.left.data)
            
    def __str__(self):
        """Represent board as string"""
        result = ''
        for row in self.board:
            for cell in row:
                if str(cell) == '-1':
                    result += str(cell)
                else:
                    result += ' ' + str(cell)
            result += '\n'
        return result
