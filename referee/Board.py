class BoardGame:
    def __init__(self, size, board, room_id, match_id, team1_id="xx1+x", team2_id="xx2+o"):
        self.size = size
        self.status = None
        self.team1_time = 0
        self.team2_time = 0
        self.score1 = 0
        self.score2 = 0
        self.board = board
        self.game_info = {
            "room_id": room_id,
            "match_id": match_id,
            "status": self.status,
            "size": size,
            "board": self.board,
            "time1": self.team1_time,
            "time2": self.team2_time,
            "team1_id": team1_id,
            "team2_id": team2_id,
            "turn": team1_id,
            "score1": self.score1,
            "score2": self.score2
        }

    def init_board(self):
        board = []
        for i in range(self.size):
            board.append([])
            for j in range(self.size):
                board[i].append(' ')
        return board

    def is_win(self, board):
        # new_board = self.convert_board(board)
        new_board = board
        print("New board: ", new_board)
        black = self.score_of_col(new_board, 'x')
        white = self.score_of_col(new_board, 'o')

        self.sum_sumcol_values(black)
        self.sum_sumcol_values(white)

        if 5 in black and black[5] == 1:
            return 'X won'
        elif 5 in white and white[5] == 1:
            return 'O won'

        if sum(black.values()) == black[-1] and sum(white.values()) == white[-1] or self.possible_moves(board) == []:
            return 'Draw'

        return 'Continue playing'

    def check_status(self, board):
        win_check = self.is_win(board)
        if win_check == 'X won' or win_check == 'O won':
            self.status = win_check
            self.game_info["status"] = self.status
            print("Result: " + win_check)
            return
        elif win_check == 'Draw':
            flag = True
            # Check if there is no free space
            for i in range(self.size):
                for j in range(self.size):
                    if board[i][j] == " ":
                        flag = False

            if flag:
                if self.game_info["time1"] < self.game_info["time2"]:
                    self.status = self.game_info["team1_id"][-1].upper() + " won"
                elif self.game_info["time1"] > self.game_info["time2"]:
                    self.status = self.game_info["team2_id"][-1].upper() + " won"
                self.game_info["status"] = self.status
                print("Draw and compare time: " + self.status)
                return
        # else:
        #     print("Continue playing")

    def make_empty_board(self, sz):
        board = []
        for i in range(sz):
            board.append([" "] * sz)
        return board

    def is_empty(self, board):
        return board == [[' '] * len(board)] * len(board)

    def is_in(self, board, y, x):
        return 0 <= y < len(board) and 0 <= x < len(board)

    def score_ready(self, scorecol):
        '''
        Khởi tạo hệ thống điểm

        '''
        sumcol = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
        for key in scorecol:
            for score in scorecol[key]:
                if key in sumcol[score]:
                    sumcol[score][key] += 1
                else:
                    sumcol[score][key] = 1

        return sumcol

    def sum_sumcol_values(self, sumcol):
        '''
        hợp nhất điểm của mỗi hướng
        '''

        for key in sumcol:
            if key == 5:
                sumcol[5] = int(1 in sumcol[5].values())
            else:
                sumcol[key] = sum(sumcol[key].values())

    def score_of_col(self, board, col):
        '''
        tính toán điểm số mỗi hướng của column dùng cho is_win;
        '''

        f = len(board)
        # scores của 4 hướng đi
        scores = {(0, 1): [], (-1, 1): [], (1, 0): [], (1, 1): []}
        for start in range(len(board)):
            scores[(1, 0)].extend(self.score_of_row(board, (0, start), 1, 0, (f - 1, start), col))
            scores[(0, 1)].extend(self.score_of_row(board, (start, 0), 0, 1, (start, f - 1), col))
            scores[(1, 1)].extend(self.score_of_row(board, (start, 0), 1, 1, (f - 1, f - 1 - start), col))
            scores[(-1, 1)].extend(self.score_of_row(board, (start, 0), -1, 1, (0, start), col))

            if start + 1 < len(board):
                scores[(1, 1)].extend(self.score_of_row(board, (0, start + 1), 1, 1, (f - 2 - start, f - 1), col))
                scores[(-1, 1)].extend(self.score_of_row(board, (f - 1, start + 1), -1, 1, (start + 1, f - 1), col))

        return self.score_ready(scores)

    def score_of_list(self, lis, col):
        blank = lis.count(' ')
        filled = lis.count(col)

        if blank + filled < 5:
            return -1
        elif blank == 5:
            return 0
        else:
            return filled

    def score_of_row(self, board, cordi, dy, dx, cordf, col):
        '''
        trả về một list với mỗi phần tử đại diện cho số điểm của 5 khối

        '''
        colscores = []
        y, x = cordi
        yf, xf = cordf
        row = self.row_to_list(board, y, x, dy, dx, yf, xf)
        for start in range(len(row) - 4):
            score = self.score_of_list(row[start:start + 5], col)
            colscores.append(score)

        return colscores

    def possible_moves(self, board):
        '''
        khởi tạo danh sách tọa độ có thể có tại danh giới các nơi đã đánh phạm vi 3 đơn vị
        '''
        # mảng taken lưu giá trị của người chơi và của máy trên bàn cờ
        taken = []
        # mảng directions lưu hướng đi (8 hướng)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        # cord: lưu các vị trí không đi 
        cord = {}

        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != ' ':
                    taken.append((i, j))
        ''' duyệt trong hướng đi và mảng giá trị trên bàn cờ của người chơi và máy, kiểm tra nước không thể đi(trùng với 
        nước đã có trên bàn cờ)
        '''
        for direction in directions:
            dy, dx = direction
            for coord in taken:
                y, x = coord
                for length in [1, 2, 3, 4]:
                    move = self.march(board, y, x, dy, dx, length)
                    if move not in taken and move not in cord:
                        cord[move] = False
        return cord

    def row_to_list(self, board, y, x, dy, dx, yf, xf):
        """
        trả về list của y,x từ yf,xf

        """
        row = []
        while y != yf + dy or x != xf + dx:
            row.append(board[y][x])
            y += dy
            x += dx
        return row

    def march(self, board, y, x, dy, dx, length):
        '''
        tìm vị trí xa nhất trong dy,dx trong khoảng length

        '''
        yf = y + length * dy
        xf = x + length * dx
        # chừng nào yf,xf không có trong board
        while not self.is_in(board, yf, xf):
            yf -= dy
            xf -= dx

        return yf, xf

    '''
    deprecated
    '''

    def convert_board(self, board):
        new_board = []
        for i in range(len(board)):
            row = []
            row.append(board[i][0])
            if i % self.size - 1 == 0:
                new_board.append(row)
        return new_board
        # self.board = board
        # self.game_info["board"] = self.board

# if __name__=="__main__":
#     game = BoardGame(5, "123", "234")
#     game.convert_board()
#     print(game.is_win(game.board))
# print(game.board)
