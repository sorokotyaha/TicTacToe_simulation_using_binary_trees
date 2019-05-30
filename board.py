import ctypes


# Implements the Array ADT using array capabilities of the ctypes module.

class Array:
    # Creates an array with size elements.
    def __init__(self, size):
        assert size > 0, "Array size must be > 0"
        self._size = size
        # Create the array structure using the ctypes module.
        PyArrayType = ctypes.py_object * size
        self._elements = PyArrayType()
        # Initialize each element.
        self.clear(None)

    # Returns the size of the array.
    def __len__(self):
        return self._size

    # Gets the contents of the index element.
    def __getitem__(self, index):
        assert index >= 0 and index < len(self), "Array subscript out of range"
        return self._elements[index]

    # Puts the value in the array element at index position.
    def __setitem__(self, index, value):
        assert index >= 0 and index < len(self), "Array subscript out of range"
        self._elements[index] = value

    # Clears the array by setting each element to the given value.
    def clear(self, value):
        for i in range(len(self)):
            self._elements[i] = value

    # Returns the array's iterator for traversing the elements.
    def __iter__(self):
        return _ArrayIterator(self._elements)


# An iterator for the Array ADT.
class _ArrayIterator:
    def __init__(self, the_array):
        self._array_ref = the_array
        self._cur_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._cur_index < len(self._array_ref):
            entry = self._array_ref[self._cur_index]
            self._cur_index += 1
            return entry
        else:
            raise StopIteration


# Implementation of the Array2D ADT using an array of arrays.

class Array2D:
    # Creates a 2 -D array of size numRows x numCols.
    def __init__(self, num_rows, num_cols):
        # Create a 1 -D array to store an array reference for each row.
        self.rows = Array(num_rows)

        # Create the 1 -D arrays for each row of the 2 -D array.
        for i in range(num_rows):
            self.rows[i] = Array(num_cols)

    # Returns the number of rows in the 2 -D array.
    def num_rows(self):
        return len(self.rows)

    # Returns the number of columns in the 2 -D array.
    def num_cols(self):
        return len(self.rows[0])

    # Clears the array by setting every element to the given value.
    def clear(self, value):
        for row in range(self.num_rows()):
            row.clear(value)

    # Checks if the indexes are positive and less than max size
    def check_index(self, row, col):
        if row >= 0 and row < self.num_rows() \
                and col >= 0 and col < self.num_cols():
            return True
        return False

    # Gets the contents of the element at position [i, j]
    def __getitem__(self, index_tuple):
        assert len(index_tuple) == 2, "Invalid number of array subscripts."
        row = index_tuple[0]
        col = index_tuple[1]
        if not self.check_index(row, col):
            return None
        array_1d = self.rows[row]
        return array_1d[col]

    # Sets the contents of the element at position [i,j] to value.
    def __setitem__(self, index_tuple, value):
        assert len(index_tuple) == 2, "Invalid number of array subscripts."
        row = index_tuple[0]
        col = index_tuple[1]
        if self.check_index(row, col):
            array_1d = self.rows[row]
            array_1d[col] = value


class Board:
    """
    Implements the LifeGrid ADT for use with the Game of Life.
    """
    # Defines constants to represent the cell states.
    ZERO_CELL = 0
    CROSS_CELL = 1

    def __init__(self, num_rows, num_cols):
        """
        Creates the game grid and initializes the cells to dead.

        :param num_rows: the number of rows.
        :param num_cols: the number of columns.
        """
        # Allocates the 2D array for the grid.
        self._grid = Array2D(num_rows, num_cols)
        # Clears the grid and set all cells to dead.
        self.configure(list())

    def numRows(self):
        """
        Returns the number of rows in the grid.

        :return: the number rows in the grid.
        """
        return self._grid.num_rows()

    def numCols(self):
        """
        Returns the number of columns in the grid.

        :return:Returns the number of columns in the grid.
        """
        return self._grid.num_cols()

    def configure(self, coord_list, value=None):
        """
        Configures the grid to contain the given value cells.
        :param coord_list: list
        :return: Board
        """
        if not coord_list:
            return self
        # Set the indicated cells to be alive.
        for coord in coord_list:
            self._grid[coord[0], coord[1]] = value
        return self
       

    def is_cross_cell(self, row, col):
        """
        Does the indicated cell contain a live organism?

        :param row: row of the cell.
        :param col: column of the cell.
        :return: the result of check.
        """
        return self._grid[row, col] == Board.CROSS_CELL

    def is_zero_cell(self, row, col):
        """
        Does the indicated cell contain a live organism?

        :param row: row of the cell.
        :param col: column of the cell.
        :return: the result of check.
        """
        return self._grid[row, col] == Board.ZERO_CELL


    def clear_cell(self, row, col):
        """
        Clears the indicated cell by setting it to None.

        :param row: row of the cell.
        :param col: column of the cell.
        """
        self._grid[row, col] = None

    def set_cross_cell(self, row, col):
        """
        Sets the indicated cell to cross.

        :param row: row of the cell.
        :param col: column of the cell.
        """
        self._grid[row, col] = Board.CROSS_CELL

    def set_zero_cell(self, row, col):
        """
        Sets the indicated cell to zero.

        :param row: row of the cell.
        :param col: column of the cell.
        """
        self._grid[row, col] = Board.CROSS_CELL

    def get_free_cells(self):
        """
        Returns the list of coordinate tuples of free cells in
        Board or an empty list if there is no free cells
        :return: list
        """
        free_cells = []
        for row in range(self.numRows()):
            for col in range(self.numCols()):
                if self._grid[row, col] == None:
                    free_cells.append((row, col))
        return free_cells
    
    def is_full(self):
        """
        Returns True if there is no more free cells left
        and False otherwise
        :return: bool
        """
        if not self.get_free_cells():
            return True
        return False

    def check_for_win_combos(self, value=None):
        """
        This method checks if there are three cells of the value type
        (ZERO_CELL by default)
        in a row, column or diagonally. Returns True if there is, False otherwise
        :return: bool
        """
        if not value:
            value = Board.ZERO_CELL
        # check center position
        if self._grid[1, 1] == value:
            # check diagonals
            if self._grid[0, 0] == self._grid[2, 2] == value or\
               self._grid[0, 2] == self._grid[2, 0] == value:
                return True
            # check cross
            if self._grid[0, 1] == self._grid[2, 1] == value or\
               self._grid[1, 0] == self._grid[1, 2] == value:
                return True
        else:
            # check for side columns and side rows
            if (self._grid[0,0] == self._grid[0, 1] == value and\
                self._grid[0, 2] == value) or (self._grid[2, 0] == value and\
                self._grid[2, 1] == self._grid[2, 2] == value):
                return True
            if (self._grid[0, 0] == self._grid[1, 0] and\
                self._grid[2, 0] == value) or (self._grid[0, 2] == value and\
                self._grid[1, 2] == self._grid[2, 2] == value):
                return True
        return False
    

    def __str__(self):
        line = ''
        for y in range(self.numRows()):
            for x in range(self.numCols()):
                if self.is_cross_cell(x, y):
                    line += "X "
                elif self.is_zero_cell(x, y):
                    line += "0 "
                else:
                    line += "- "
            line += "\n"
        return line


    def get_cross_cells(self):
        """
        Returns the list of coordinate tuples of cross cells in
        Board or an empty list if there is no cross cells
        :return: list
        """
        cross_cells = []
        for row in range(self.numRows()):
            for col in range(self.numCols()):
                if self.is_cross_cell(row, col):
                    cross_cells.append((row, col))
        return cross_cells


    def get_zero_cells(self):
        """
        Returns the list of coordinate tuples of cross cells in
        Board or an empty list if there is no cross cells
        :return: list
        """
        zero_cells = []
        for row in range(self.numRows()):
            for col in range(self.numCols()):
                if self.is_zero_cell(row, col):
                    zero_cells.append((row, col))
        return zero_cells
