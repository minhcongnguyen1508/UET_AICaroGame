from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify, make_response
# from flask_socketio import SocketIO
import json
import time
from Board import BoardGame

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# socketio = SocketIO(app, cors_allowed_origins="*")

# Global variance
PORT=1724
team1_id = "xx1"
team2_id = "xx2"
team1_role = "x"
team2_role = "o"
room_id = "123"
match_id = "321"
size = 5
#################

time_list = [time.time()] * 2
start_game = False

board = []
for i in range(size):
    board.append([])
    for j in range(size):
        board[i].append(' ')


team1_id_full = team1_id + "+" + team1_role
team2_id_full = team2_id + "+" + team2_role
board_game = BoardGame(size, board, room_id, match_id, team1_id_full, team2_id_full)

@app.route('/init', methods=['POST'])
@cross_origin()
def get_data():
    data  = request.data
    info = json.loads(data.decode('utf-8'))
    return {
        "room_id": board_game.game_info["room_id"],
        "match_id": board_game.game_info["match_id"],
        "init": True, 
        }


@app.route('/', methods=['POST'])
@cross_origin()
def render_board():
    data  = request.data
    info = json.loads(data.decode('utf-8'))
    # print(info['team_id'])
    global start_game
    if(info["team_id"] == team1_id_full and not start_game):
        time_list[0] = time.time()
        start_game = True
    # print(f'Board: {board_game.game_info["board"]}')
    response = make_response(jsonify(board_game.game_info))
    return board_game.game_info

@app.route('/')
@cross_origin()
def fe_render_board():
    # print(board_game.game_info)
    response = make_response(jsonify(board_game.game_info))
    # print(board_game.game_info)
    return response


@app.route('/move', methods=['POST'])
@cross_origin()
def handle_move():
    data = request.data

    data = json.loads(data.decode('utf-8'))
    print(f'Board: {data["board"]}')
    if data["turn"] == board_game.game_info["turn"] and data["status"] == None:
        board_game.game_info.update(data)
        if data["turn"] == team1_id_full:
            board_game.game_info["time1"] += time.time() - time_list[0]
            board_game.game_info["turn"] = team2_id_full
            time_list[1] = time.time()
        else:
            board_game.game_info["time2"] += time.time() - time_list[1]
            board_game.game_info["turn"] = team1_id_full
            time_list[0] = time.time()
    print("Team 1 time: ", time_list[0])
    print("Team 2 time: ", time_list[1])
    if data["status"] == None:
        print("Checking status...")
        board_game.check_status(data["board"])
    # print("After check status: ",board_game.game_info)

    # board_game.convert_board(board_game.game_info["board"])
    
    return 'ok'


if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0", port=PORT)