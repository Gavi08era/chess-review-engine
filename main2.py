import chess
import chess.engine
import chess.pgn
from pathlib import Path
import re
class game_analyzer:
    def __init__(self, ):
        pass
class Move_analysis:
    def __init__(self):
        pass
class engine_wrapper:
    def __init__(self):
        pass

def main():
    game = load_game()
    engine = initialize_engine()
    try:
        analyze_game(game, engine)
    finally:
        engine.quit()


def load_game():
    with open("Carlsen.pgn", "r", encoding="utf-8") as pgn:
        game = chess.pgn.read_game(pgn)

    if game is None:
        raise ValueError("No valid game found in Carlsen.pgn")

    return game


def initialize_engine():
    engine_path = (
        Path(__file__).resolve().parent
        / "stockfish-windows-x86-64-avx2"/ "stockfish"/ "stockfish-windows-x86-64-avx2.exe")

    if not engine_path.exists():
        raise FileNotFoundError(f"Stockfish executable not found: {engine_path}")

    return chess.engine.SimpleEngine.popen_uci(str(engine_path))


def analyze_game(game, engine):
    board = game.board()

    for move in game.mainline_moves():
        engine_move(board, engine)
        san = board.san(move)
        print("Pre-move_eval: ", evalBeforeMove(board, engine))
        print("Player move: ", san)
        
        board.push(move)
        print(board)
        print("Post-move_eval", evalAfterMove(board, engine))
        eval_drop(board, engine)
        print("")


def evalBeforeMove(board, engine):
    info = engine.analyse(board, chess.engine.Limit(time=0.1))
    return universal_score(info)
    #pre_eval=regex_problem(info)
    #return pre_eval

def evalAfterMove(board, engine):
    info = engine.analyse(board, chess.engine.Limit(time=0.1))
    return universal_score(info)
    #pre_eval = regex_problem(info)
    #return pre_eval


def universal_score(info):
    # Fixed perspective: positive means White is better, negative means Black is better.
    return info["score"].pov(chess.WHITE)
def regex_problem(info):
    match = re.findall(r'Cp\((-?\d+)\)', universal_score(info))
    value = [int(x) for x in match]
    return value

def engine_move(board, engine):
    result = engine.play(board, chess.engine.Limit(depth=15))
    san=board.san(result.move)
    board.push(result.move)
    print("Engine Move: ", san)
    engine_eval(engine, board)
    board.pop()

def engine_eval(engine, board):
    info = engine.analyse(board, chess.engine.Limit(time=0.1))
    print("Engine_Evaluation:", universal_score(info))


#eval drop
#classify move
#eval bar
def eval_drop(board, engine):
    pass
    #post_eval-pre_eval=+-drop
    #drop=evalBeforeMove(board, engine)-evalAfterMove(board, engine)
    #print(drop)




if __name__ == "__main__":
    main()
