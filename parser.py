import chess.pgn
import chess

class parsing_pgn:
    def load_game():
        
        filepath=input("Enter pgn file path")
        with open(filepath, "r", encoding="utf-8") as pgn:
            game = chess.pgn.read_game(pgn)

        if game is None:
            raise ValueError("No valid game found in Carlsen.pgn")

        return game
    
    @staticmethod
    def played_moves(game):
        board=chess.Board()
        uci_moves = list(game.mainline_moves())
        uci_history=[]
        san_history=[]
        for move in uci_moves:
            uci_history.append(move)
            board.push(move)
            

        return uci_history

    def get_players(game):
        white_player = game.headers["White"]
        black_player = game.headers["Black"]
        return (white_player, black_player)
    
    def get_date(game):
        return game.headers["Date"]
    
    def get_result(game):
        game_result =game.headers["Result"]
        return game_result
    
    def san_moves(game):
        board=chess.Board()
        uci_moves=list(game.mainline_moves())
        san_history=[]
        for move in uci_moves:
            san_move = board.san(move)
            san_history.append(san_move)
            board.push(move)
        return san_history
    def proper_notation(game):
        return str(game.mainline_moves())

        


if __name__=="__main__":
    obj=parsing_pgn
    game=obj.load_game()
    move_list=obj.played_moves(game)
    #uci_list=obj.uci_to_san(game)
    san_list=obj.san_moves(game)

    
    print(obj.proper_notation(game))
    #print(uci_list)

