import chess
import chess.engine
from pathlib import Path
board=chess.Board()
def initialize_engine():
    # Resolve the bundled Stockfish executable relative to this script.
    engine_path = (
        Path(__file__).resolve().parent
        / "stockfish-windows-x86-64-avx2"/ "stockfish"/ "stockfish-windows-x86-64-avx2.exe")

    if not engine_path.exists():
        raise FileNotFoundError(f"Stockfish executable not found: {engine_path}")

    return chess.engine.SimpleEngine.popen_uci(str(engine_path))

engine=initialize_engine()

class engine_func:
    @staticmethod
    def universal_score(info):
        # Fixed perspective: positive means White is better, negative means Black is better.
        return info["score"].pov(chess.WHITE).score(mate_score=100000)


    def eval(board, engine):
        # Ask Stockfish for the current position evaluation before the move is played.
        info = engine.analyse(board, chess.engine.Limit(time=0.1))
        return engine_func.universal_score(info)
    

    def engine_move(board, engine):
        # Get the engine's best move and convert it to SAN for display.
        result = engine_func.engine.play(board, chess.engine.Limit(depth=15))
        return board.san(result.move)
    def engine_exit(engine):
        engine.quit()