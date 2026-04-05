import chess
import chess.pgn
from pathlib import Path


with open("Carlsen.pgn", "r", encoding="utf-8") as pgn:
    game = chess.pgn.read_game(pgn)
if game is None:
    raise ValueError("No valid game found in Carlsen.pgn")

board = game.board()

import chess.engine
engine_path = Path(__file__).resolve().parent / "stockfish-windows-x86-64-avx2" / "stockfish" / "stockfish-windows-x86-64-avx2.exe"
engine = chess.engine.SimpleEngine.popen_uci(str(engine_path))

for move in game.mainline_moves():
    san=board.san(move)
    print(san)
    board.push(move)
    print(board)
    info = engine.analyse(board, chess.engine.Limit(time=0.1))
    print("Evaluation:", info["score"])
    result = engine.play(board, chess.engine.Limit(depth=15))
    print("Best Move: ", san(result.move))

    print("")



    