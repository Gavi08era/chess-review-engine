import chess
import chess.engine
import chess.pgn
from pathlib import Path
import re
import json
import csv


class game_analyzer:
    def __init__(self, ):
        # Placeholder class for future game-level analysis state.
        pass
class Move_analysis:
    def __init__(self):
        # Placeholder class for storing data about a single move.
        pass
class engine_wrapper:
    def __init__(self):
        # Placeholder class for wrapping engine setup and calls.
        pass


def main():
    # Load the input game, connect to Stockfish, analyze the game, then close the engine.
    game = load_game(filepath)
    engine = initialize_engine()
    try:
        game_analysis = analyze_game(game, engine)
        #save_analysis(game_analysis)
    finally:
        engine.quit()
filepath=input("Enter PGN file path: ")




def load_game(filepath: str):
    # Read the first PGN game from the file and fail fast if the file is empty or invalid.
    with open(filepath, "r", encoding="utf-8") as pgn:
        game = chess.pgn.read_game(pgn)

    if game is None:
        raise ValueError("No valid game found in Carlsen.pgn")

    return game




def initialize_engine():
    # Resolve the bundled Stockfish executable relative to this script.
    engine_path = (
        Path(__file__).resolve().parent
        / "stockfish-windows-x86-64-avx2"/ "stockfish"/ "stockfish-windows-x86-64-avx2.exe")

    if not engine_path.exists():
        raise FileNotFoundError(f"Stockfish executable not found: {engine_path}")

    return chess.engine.SimpleEngine.popen_uci(str(engine_path))


def analyze_game(game, engine):
    # Walk through the mainline moves and compare the played move with engine evaluations.
    board = game.board()
    move_count = 0
    game_analysis = []
    eval_timeline=[] 
    eval_bar_white=[]   #eval_bar


    # Pull player names from the PGN headers for reporting.
    white_player = game.headers["White"]
    black_player = game.headers["Black"]
    print(f"White: {white_player}, Black: {black_player}")

    for move in game.mainline_moves():
        move_count += 1

        # Capture the engine position before the move is pushed.
        pre_eval = evalBeforeMove(board, engine)
        # Get the engine's preferred move for the current board.
        best_move = engine_move(board, engine)
        # Convert the played move to SAN notation for readable output.
        played_move = player_move(board, move)
        

        print(f"Move {move_count}")
        print("Pre_move eval:", pre_eval)
        print("Best move:", best_move)
        print("Player move:", played_move)

        # Advance the board to the played move so the next evaluation is on the new position.
        board.push(move)
        print(board)

        # Evaluate the new position after the move has been played.
        post_eval = evalAfterMove(board, engine)
        print("Post_move_eval:", post_eval)

        # Measure how much the position changed and label the quality of the move.
        drop = eval_drop(pre_eval, post_eval)
        classification = move_classification(pre_eval, post_eval)
        print("Evaluation drop:", drop)
        print("Move Classification:", classification)

        # Store the per-move analysis in a dictionary for later reporting or export.
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


        # Track a simple timeline of evaluation changes for summary metrics.
        eval_timeline.append(drop/100)
        eval_bar_white.append(to_percentage(drop, min_val=-5, max_val=5))



        print("")
    print(eval_timeline)
    print("")
    print(eval_bar_white)
    print("")
    accuracy(eval_timeline)
    summary=game_summary(game_analysis)
    print(summary)
    game_result(game)

    #write down no. of moves
    return game_analysis

def player_move(board, move):
    # Convert the move object into standard algebraic notation.
    san=board.san(move)
    return san

def board_print(board,move):
    # Utility helper for printing the board after applying a move.
    player_move(board, move)
    board.push(move)
    return board

def evalBeforeMove(board, engine):
    # Ask Stockfish for the current position evaluation before the move is played.
    info = engine.analyse(board, chess.engine.Limit(time=0.1))
    return universal_score(info)
    #pre_eval=regex_problem(info)
    #return pre_eval

def evalAfterMove(board, engine):
    # Ask Stockfish for the new position evaluation after the move has been played.
    info = engine.analyse(board, chess.engine.Limit(time=0.1))
    return universal_score(info)
    #pre_eval = regex_problem(info)
    #return pre_eval


def universal_score(info):
    # Fixed perspective: positive means White is better, negative means Black is better.
    return info["score"].pov(chess.WHITE).score(mate_score=100000)

def engine_move(board, engine):
    # Get the engine's best move and convert it to SAN for display.
    result = engine.play(board, chess.engine.Limit(depth=15))
    return board.san(result.move)

def engine_eval(engine, board):
    # Print a one-off engine evaluation for the current position.
    info = engine.analyse(board, chess.engine.Limit(time=0.2))
    print("Engine_Evaluation:", universal_score(info))


#eval drop done
#classify move
#eval bar
def eval_drop(pre_eval, post_eval):
    # Use absolute difference as a simple measure of how much the position changed.
    drop = abs(pre_eval - post_eval)
    return drop

def move_classification(pre_eval, post_eval):
    # Convert the evaluation swing into a rough move-quality label.
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
    # Package all move information into a single record.
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
    # Map the evaluation drop into a 0-100 scale for a visual bar or score display.
    return (((drop/100) - min_val) / (max_val - min_val)) * 100
    
#def save_analysis(game_analysis):
    #output_path = Path(__file__).resolve().parent / "notes" / "analysis_data.json"
    #output_path.parent.mkdir(parents=True, exist_ok=True)
    #with open(output_path, "w", encoding="utf-8") as f:
    #json.dump(game_analysis, f, indent=2, ensure_ascii=False)
    #print(f"Saved analysis to: {output_path}")



def color(move_number):
    # Odd move numbers belong to White, even move numbers belong to Black.
    if move_number % 2 == 1:
        return "White"
    return "Black"

def game_summary(game_analysis):
    # Aggregate move-quality labels separately for White, Black, and the full game.
    labels = ["Best", "Excellent", "Good", "Inaccuracy", "Mistake", "Blunder"]

    summary = {
        "White": {label: 0 for label in labels},
        "Black": {label: 0 for label in labels},
        "Total": {label: 0 for label in labels},
    }

    for move_data in game_analysis:
        move_number = move_data.get("move_number")
        classification = move_data.get("classification")

        # Skip malformed records that do not have the expected fields.
        if not isinstance(move_number, int) or classification not in summary["Total"]:
            continue

        side = color(move_number)
        summary[side][classification] += 1
        summary["Total"][classification] += 1

    return summary

def game_result(game):
    # Print the final result as recorded in the PGN headers.
    result=game.headers["Result"]
    print(f"Result: {result}")
    if result.strip()=="0-1":
        print("Black Won")
    elif result.strip()=="1-0":
        print("White Won")
    else:
        print("Draw")
    
#todo

#Brilliant moves
#Great Moves
#Opening Detection
#book moves
#missed moves(missed tactics)
#prining mate in n
#performance elo

#Accuracy(overalll for black and white, opening, middle game and end game)
#avg(drop)*100
def accuracy(eval_timeline):
    # Split the timeline by side to produce a rough white/black accuracy estimate.
    w=[]
    b=[]
    for i, value in enumerate(eval_timeline):
        if i%2==0:
            w.append(value)
        else:
            b.append(value)
    print("white: ", average(w))
    print("Black", average(b))
            # Convert the raw list into a simple average-based score.





            # Read opening names and print each CSV row for inspection.
def average(arr):
    avg=sum(arr)/len(arr)

    return 100-avg*10

    
            # Placeholder for opening classification logic.
    with open('chess_openings.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
    for row in reader:
        print(row)

def opening_detection():
    
    pass


if __name__ == "__main__":
    main()