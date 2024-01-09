from copy import deepcopy as copy
import argparse
from animation import draw


class Node():
    def __init__(self, board, jumpfrom=None, jumpover=None, jumpto=None):
        self.board = board
        self.jumpfrom = jumpfrom
        self.jumpover = jumpover
        self.jumpto = jumpto


class peg:
    def __init__(self, start_row, start_col, rule):
        self.size = 5
        self.start_row, self.start_col, self.rule = start_row, start_col, rule
        # board
        self.board = [[1 for j in range(i + 1)] for i in range(self.size)]
        self.board[start_row][start_col] = 0
        self.start = Node(copy(self.board))
        # path
        self.path = []
        self.path.append(Node(copy(self.board)))
        # Do some initialization work here if you need:

    def draw(self):
        if self.success():
            draw(self.path, self.start_row, self.start_col, self.rule)
        else:
            print("No solution were found!")

    def boundary(self, row, col):
        if row > 4 or col > 4:
            return False
        if row < 0 or col < 0:
            return False
        if row == 0 and col > 0:
            return False
        if row == 1 and col > 1:
            return False
        if row == 2 and col > 2:
            return False
        if row == 3 and col > 3:
            return False
        if row == 4 and col > 4:
            return False
        else:
            return True

    def sucessor(self):
        successors = []
        y = 0
        for row in range(5):  # go thru list in board
            y += 1  # increment column each time
            for column in range(y):  # go thru value in the list
                if self.board[row][column] == 1:  # if the value is 1
                    if self.boundary(row, column + 2):
                        if self.board[row][column + 1] == 1:
                            if self.board[row][column + 2] == 0:  # check if two steps to the right is 0
                                jumpFrom = (row, column)
                                jumpTo = (row, column + 2)
                                jumpOver = (row, column + 1)

                                successors.append([jumpTo, jumpOver, jumpFrom])
                    if self.boundary(row, column - 2):  # if u go back twice , there should be a column greater than 0
                        if self.board[row][column - 1] == 1:
                            if self.board[row][column - 2] == 0:  # check if two steps to the left is 1
                                jumpFrom = (row, column)
                                jumpTo = (row, column - 2)
                                jumpOver = (row, column - 1)
                                successors.append([jumpTo, jumpOver, jumpFrom])

                    if self.boundary((row + 2), column):  # down diagonal left , # 4 is the index of row
                        if self.board[row + 1][column] == 1:
                            if self.board[row + 2][column] == 0:  # cehck if two steps below is 1
                                jumpFrom = (row, column)
                                jumpTo = (row + 2, column)
                                jumpOver = (row + 1, column)
                                successors.append([jumpTo, jumpOver, jumpFrom])

                    if self.boundary(row + 2, column + 2):  # down diagonal right
                      if self.board[row + 1][column+1] == 1:
                        if self.board[row + 2][column + 2] == 0:  # cehck if two steps below is 1
                            jumpFrom = (row, column)
                            jumpTo = (row + 2, column + 2)
                            jumpOver = (row + 1, column + 1)
                            successors.append([jumpTo, jumpOver, jumpFrom])

                    if self.boundary((row - 2), column):  # up diagnoal right column will be the same
                      if self.board[row - 1][column] == 1:
                        if self.board[row - 2][column] == 0:
                            jumpFrom = (row, column)
                            jumpTo = (row - 2, column)
                            jumpOver = (row - 1, column)
                            successors.append([jumpTo, jumpOver, jumpFrom])

                    if self.boundary(row - 2, column - 2):  # up diagnoal left , don't go past the oth index
                      if self.board[row - 1][column - 1] == 1:
                        if self.board[row - 2][column - 2] == 0:  # cehck if two steps above is 1
                            jumpFrom = (row, column)
                            jumpTo = (row - 2, column - 2)
                            jumpOver = (row - 1, column - 1)
                            successors.append([jumpTo, jumpOver, jumpFrom])

        return successors  # returns boards

    def success(self):
        count = 0
        for row in self.board:
            for col in row:  # list inside the list
                if col == 1:  # if we've 1 at a position of y in the list  increase count by 1
                    count += 1
        if count == 1:  # if there was only one 1 then we've found the solution
            return True
        else:
            return False

    def solve(self):

        if self.success():
            return True
        # starting board with all other parameters as none
        successors = self.sucessor()

        for jump in successors:  # all the diff jumps we can make

            node = Node(self.board, jump[2], jump[1], jump[0])

            self.board[node.jumpfrom[0]][node.jumpfrom[1]] = 0
            self.board[node.jumpto[0]][node.jumpto[1]] = 1
            self.board[node.jumpover[0]][node.jumpover[1]] = 0  # we have node with new board and everything
            node.board = copy(self.board)
            self.path.append(node)

            if self.solve():
                return True

            self.path.pop()
            self.board[node.jumpfrom[0]][node.jumpfrom[1]] = 1
            self.board[node.jumpto[0]][node.jumpto[1]] = 0
            self.board[node.jumpover[0]][node.jumpover[1]] = 1
            node.board = copy(self.board)




        return False  # if no more sucessors


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='peg game')

    parser.add_argument('-hole', dest='position', required=True, nargs='+', type=int,
                        help='initial position of the hole')
    parser.add_argument('-rule', dest='rule', required=True, type=int, help='index of rule')

    args = parser.parse_args()

    start_row, start_col = args.position
    if start_row > 4:
        print("row must be less or equal than 4")
        exit()
    if start_col > start_row:
        print("column must be less or equal than row")
        exit()

    # Example:
    # python peg.py -hole 0 0 -rule 0
    game = peg(start_row, start_col, args.rule)
    game.solve()
    game.draw()




# random comment
# another
for x in  range(5):
    print(2)
