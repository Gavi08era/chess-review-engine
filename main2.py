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
        pre_eval = evalBeforeMove(board, engine)
        print("Pre_move eval: ", pre_eval)
        print("Player move: ", san)
        
        board.push(move)
        post_eval = evalAfterMove(board, engine)
        print(board)
        print("post_move_eval", post_eval)
        print("Evaluation drop", eval_drop(pre_eval, post_eval))
        print("Move Classification:", move_classification(pre_eval, post_eval))
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
    return info["score"].pov(chess.WHITE).score(mate_score=100000)
def regex_problem(info):
    match = re.findall(r'Cp\((-?\d+)\)', universal_score(info))
    value = [int(x) for x in match]
    return int(value)

def engine_move(board, engine):
    result = engine.play(board, chess.engine.Limit(depth=15))
    san=board.san(result.move)
    board.push(result.move)
    print("Engine Move: ", san)
    engine_eval(engine, board)
    board.pop()

def engine_eval(engine, board):
    info = engine.analyse(board, chess.engine.Limit(time=0.2))
    print("Engine_Evaluation:", universal_score(info))


#eval drop done
#classify move
#eval bar
def eval_drop(pre_eval, post_eval):
    drop = pre_eval - post_eval
    return drop

def move_classification(pre_eval, post_eval):
    if -30<=eval_drop(pre_eval, post_eval) <=30:
        return "Good"
    elif -30<eval_drop(pre_eval, post_eval)<=70 or -70<=eval_drop(pre_eval, post_eval)<-30:
        return "Inaccuracy"
    elif 70<eval_drop(pre_eval, post_eval)<=150 in range(70, 150) or -150<=eval_drop(pre_eval, post_eval)< -70:
        return "mistake"
    else:
        return "Blunder"




if __name__ == "__main__":
    main()
