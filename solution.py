from utils import *

# Define unit lists
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [
    [rows[i] + cols[i] for i in range(9)],  # Main diagonal
    [rows[i] + cols[8 - i] for i in range(9)]  # Anti-diagonal
]
unitlist = row_units + column_units + square_units + diagonal_units

# Extract units and peers
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)

def naked_twins(values):
    """Eliminate values using the naked twins strategy."""
    if not values:
        return False
    
    for boxA in values:
        for boxB in peers[boxA]:
            if values[boxA] == values[boxB] and len(values[boxA]) == 2:
                for peer in set(peers[boxA]) & set(peers[boxB]):
                    for digit in values[boxA]:
                        values[peer] = values[peer].replace(digit, '')
    return values

def eliminate(values):
    """Eliminate values from peers of each box with a single value."""
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
            if len(values[peer]) == 0:
                return False
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit."""
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1 and len(values[dplaces[0]]) > 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """Reduce puzzle using eliminate, only choice, and naked twins strategies."""
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if not values or len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """Solve puzzle using depth-first search and propagation."""
    values = reduce_puzzle(values)
    if not values:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    return False

def solve(grid):
    """Find the solution to a Sudoku grid."""
    values = grid2values(grid)
    values = search(values)
    return values

if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)
    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a requirement.')