from engine import Engine, Board, Move, get_pos

def get_move(move_str: str) -> Move:
    pos = get_pos(move_str[:2])
    dest = get_pos(move_str[2:])
    move = Move(pos, dest)
    
    # add promotion
    if len(move_str) > 4:
        move.prom = move_str
    
    return move


while True:
    command = input()
    args = command.split()
    
    if args[0] == "uci":
        print("id name Chess Club 7")
        print("id author Andrew")
        print("uciok")
        
    elif args[0] == "isready":
        print("readyok")
        
    elif args[0] == "position":
        if args[1] == "startpos":
            board = Board()
            for move in args[3:]:
                board.make(get_move(move))
                
        elif args[1] == "fen":
            board = Board(args[2])
            for move in args[4:]:
                board.make(get_move(move))
                
    elif args[0] == "go":
        computer = Engine()
        move = computer.search(board)
        print("bestmove", move)
     
               
    elif args[0] == "quit":
        break
            
        
            
        