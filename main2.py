import chess
import chess.engine
import chess.pgn
from pathlib import Path


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
        / "stockfish-windows-x86-64-avx2"
        / "stockfish"
        / "stockfish-windows-x86-64-avx2.exe"
    )

    if not engine_path.exists():
        raise FileNotFoundError(f"Stockfish executable not found: {engine_path}")

    return chess.engine.SimpleEngine.popen_uci(str(engine_path))


def analyze_game(game, engine):
    board = game.board()

    for move in game.mainline_moves():
        san = board.san(move)
        print(san)
        board.push(move)
        print(board)
        evaluate_position_after_move(board, engine)
        classify_move(engine, board)
        print("")


def evaluate_position_after_move(board, engine):
    info = engine.analyse(board, chess.engine.Limit(time=0.1))
    print("Evaluation:", info["score"])
    result = engine.play(board, chess.engine.Limit(depth=15))
    san_engine = board.san(result.move)
    print("Best Move:", san_engine)


def classify_move(engine, board):
    result = engine.play(board, chess.engine.Limit(depth=15))
    board.push(result.move)
    info = engine.analyse(board, chess.engine.Limit(time=0.1))
    print("Engine_Evaluation:", info["score"])
    board.pop()
if __name__ == "__main__":
    main()
