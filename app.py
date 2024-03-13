from flask import Flask, render_template, request, jsonify
import threading

app = Flask(__name__)

board = {1: " ", 2: " ", 3: " ",
         4: " ", 5: " ", 6: " ",
         7: " ", 8: " ", 9: " "}

turn = "X"
game_end = False
mode = "multiPlayer"

def check_for_win(player, current_board):
    # Check rows
    for i in range(0, 3):
        if current_board[1 + i * 3] == current_board[2 + i * 3] == current_board[3 + i * 3] == player:
            return True

    # Check columns
    for i in range(0, 3):
        if current_board[1 + i] == current_board[4 + i] == current_board[7 + i] == player:
            return True

    # Check diagonals
    if current_board[1] == current_board[5] == current_board[9] == player:
        return True
    if current_board[3] == current_board[5] == current_board[7] == player:
        return True

    return False

def check_for_draw(current_board):
    return all(value != " " for value in current_board.values())

def play_computer():
    best_score = -10
    best_move = 0
    temp_board = board.copy()

    for key in temp_board.keys():
        if temp_board[key] == " ":
            temp_board[key] = "O"
            score = minimax(temp_board, False)  # Use minimax algorithm
            temp_board[key] = " "
            if score > best_score:
                best_score = score
                best_move = key

    board[best_move] = "O"

def minimax(current_board, is_maximizing):
    if check_for_win("O", current_board):
        return 1

    if check_for_win("X", current_board):
        return -1

    if check_for_draw(current_board):
        return 0

    if is_maximizing:
        best_score = -1
        for key in current_board.keys():
            if current_board[key] == " ":
                current_board[key] = "O"
                score = minimax(current_board, False)
                current_board[key] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1
        for key in current_board.keys():
            if current_board[key] == " ":
                current_board[key] = "X"
                score = minimax(current_board, True)
                current_board[key] = " "
                best_score = min(score, best_score)
        return best_score

def game_logic(cell):
    global turn, game_end, mode
    if board[cell] == " ":
        board[cell] = turn

        if check_for_win(turn, board):
            result = f"{turn} wins the game!"
            game_end = True
        elif check_for_draw(board):
            result = "Game Draw!"
            game_end = True
        else:
            result = None

        if mode != "multiPlayer":
            if turn == "X":
                play_computer()
                if check_for_win("O", board):
                    result = "Computer wins the game!"
                    game_end = True
                elif check_for_draw(board):
                    result = "Game Draw!"
                    game_end = True
                turn = "X"
        else:
            turn = "O" if turn == "X" else "X"

        return {"result": result, "board": board, "game_end": game_end}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/play", methods=["POST"])
def play():
    cell = int(request.form["cell"])
    return jsonify(game_logic(cell))

@app.route("/restart", methods=["POST"])
def restart():
    global board, turn, game_end
    board = {1: " ", 2: " ", 3: " ",
             4: " ", 5: " ", 6: " ",
             7: " ", 8: " ", 9: " "}
    turn = "X"
    game_end = False
    return {"board": board, "turn": turn, "game_end": game_end}

@app.route("/mode", methods=["POST"])
def change_mode():
    global mode
    mode = request.form["mode"]
    return {"mode": mode}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)