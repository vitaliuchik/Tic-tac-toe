from board import Board


if __name__ == '__main__':
    board = Board()

    while board.check_results() == Board.CONTINUE:
        try:
            cell = list(map(int, str(input("Input cell coordinates (separated by space): ")).split()))
        except KeyboardInterrupt:
            print("Error: incorrect value")
            continue
        try:
            board.make_move(cell)
            print(board)
        except AssertionError as e:
            print(e)
            continue
        if board.check_results() != Board.CONTINUE:
            break
        board = board.computer_move()
        print(board)

    result = board.check_results()
    if result == Board.CROSS_WON:
        print("Player has won")
    elif result == Board.NOUGHT_WON:
        print("Computer has won")
    elif result == Board.FINISH:
        print("No one has won")