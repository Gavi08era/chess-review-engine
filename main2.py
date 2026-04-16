import chess
import chess.engine
import chess.pgn
from pathlib import Path
import re
import json



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
    game = load_game(filepath)
    engine = initialize_engine()
    try:
        game_analysis = analyze_game(game, engine)
        #save_analysis(game_analysis)
    finally:
        engine.quit()
filepath=input("Enter PGN file path: ")
def load_game(filepath: str):
    with open(filepath, "r", encoding="utf-8") as pgn:
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
    move_count = 0
    game_analysis = []
    eval_timeline=[] 
    eval_bar_white=[]   #eval_bar

    for move in game.mainline_moves():
        move_count += 1

        pre_eval = evalBeforeMove(board, engine)
        best_move = engine_move(board, engine)
        played_move = player_move(board, move)

        print(f"Move {move_count}")
        print("Pre_move eval:", pre_eval)
        print("Best move:", best_move)
        print("Player move:", played_move)

        board.push(move)
        print(board)

        post_eval = evalAfterMove(board, engine)
        print("Post_move_eval:", post_eval)

        drop = eval_drop(pre_eval, post_eval)
        classification = move_classification(pre_eval, post_eval)
        print("Evaluation drop:", drop)
        print("Move Classification:", classification)

        move_data = analysis_data(
            move_number=move_count,
            played_move=played_move,
            best_move=best_move,
            pre_eval=pre_eval,
            post_eval=post_eval,
            drop=drop,
            classification=classification,
        )
        game_analysis.append(move_data)


        eval_timeline.append(drop/100)
        eval_bar_white.append(to_percentage(drop, min_val=-5, max_val=5))



        print("")
    print(eval_timeline)
    print(eval_bar_white)

    return game_analysis

def player_move(board, move):
    san=board.san(move)
    return san

def board_print(board,move):
    player_move(board, move)
    board.push(move)
    return board

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
    return board.san(result.move)

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
    drop = abs(pre_eval - post_eval)

    if drop == 0:
        return "Best"
    elif drop<=20 or drop>=-20:
        return "Excellent"
    elif drop <= 50 or drop>=-50:
        return "Good"
    elif drop <= 100 or drop>=-100:
        return "Inaccuracy"
    elif drop <=150 or drop>=-150:
        return "Mistake"
    return "Blunder"
    

def analysis_data(move_number, played_move, best_move, pre_eval, post_eval, drop, classification):
     move_data = {
        "move_number": move_number,
        "played_move": played_move,
        "best_move": best_move,
        "eval_before": pre_eval,
        "eval_after": post_eval,
        "eval_drop": drop,
        "classification": classification,
    }
     
     return move_data



def to_percentage(drop, min_val=-5, max_val=5):
    return (((drop/100) - min_val) / (max_val - min_val)) * 100
    
#def save_analysis(game_analysis):
    #output_path = Path(__file__).resolve().parent / "notes" / "analysis_data.json"
    #output_path.parent.mkdir(parents=True, exist_ok=True)
    #with open(output_path, "w", encoding="utf-8") as f:
    #json.dump(game_analysis, f, indent=2, ensure_ascii=False)
    #print(f"Saved analysis to: {output_path}")



def color(move_number):
    if move_number % 2 == 1:
        return "White"
    return "Black"

def game_summary(game_analysis):
    labels = ["Best", "Excellent", "Good", "Inaccuracy", "Mistake", "Blunder"]

    summary = {
        "White": {label: 0 for label in labels},
        "Black": {label: 0 for label in labels},
        "Total": {label: 0 for label in labels},
    }

    for move_data in game_analysis:
        move_number = move_data.get("move_number")
        classification = move_data.get("classification")

        if not isinstance(move_number, int) or classification not in summary["Total"]:
            continue

        side = color(move_number)
        summary[side][classification] += 1
        summary["Total"][classification] += 1

    return summary




def opening_detection():
    pass
def blunder_counter():
    pass



if __name__ == "__main__":
    main()
