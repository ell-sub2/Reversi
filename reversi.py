"""
2019.03.11 設計変更
Piece:
  盤面の状態を表す。・、●、○の3状態。
Player:
  色と手持ち数を持つ。
Board:
  盤面自体の状態を持つ。Pieceとhas - a関係。
Game:
  Player、Boardとhas - a関係。
"""

class Piece:
    states = {".":"・", "black":"●", "white":"○"}

    def __init__(self, x, y):
        self.state = self.states["."] #初期状態では全ての目が"・"
        self.x = x
        self.y = y

    def set_state(self, color):
        self.state = self.states[color]

    def reverse_piece(self):  # 裏返す
        if self.state == self.states["black"]:
            self.state = self.states["white"]
        elif self.state == self.states["white"]:
            self.state = self.states["black"]
        else:
            self.state = self.states["."]

    def __str__(self):
        return self.state


class Board:
    pieces = [["" for i in range(8)] for j in range(8)]
    last_puted_rocation = [0, 0]  # x, y #これ書いてみたけど使えそう。Boardクラスで大丈夫?
    last_puted_color = None
    last_puted_piece_copy = None

    def __init__(self):
        #盤面の生成(Piece64個)
        for x in range(0, 8):
            for y in range(0, 8):
                self.pieces[y][x] = Piece(x, y)

    def __str__(self):
        stage = ""
        for y in range(0, 8):
            for x in range(0, 8):
                stage += self.pieces[y][x].state
            stage += "\n"
        return stage

    def __add__(self, another):
        return self.__str__() + another

    def is_already_put(self, x, y):
        if self.pieces[y][x].state != "・":
            return True
        else:
            return False

    def set_piece_to(self, x, y, color):  # pieceを置くときに呼ぶ
        self.pieces[y][x].set_state(color)
        self.last_puted_rocation[0] = x
        self.last_puted_rocation[1] = y
        self.last_puted_color = Piece.states[color]

    def calc_black_area(self):
        area = 0
        for y in self.pieces:
            for x in y:
                if x.state == "○":
                    area += 1
        return area

    def calc_white_area(self):
        area = 0
        for y in self.pieces:
            for x in y:
                if x.state == "●":
                    area += 1
        return area


    #"○"が更新されねえ...
    def update(self):  # boad上のpiece色を演算し、更新
        x_offset = self.last_puted_rocation[0]
        y_offset = self.last_puted_rocation[1]
        ########################################
        # 行
        ########################################
        # コマを置いた左側
        target_x_left = x_offset
        for x_left in range(x_offset - 1, -1, -1):
            if self.pieces[y_offset][x_left].state != self.last_puted_color and self.is_already_put(x_left, y_offset): #違う色なら
                continue
            if (self.pieces[y_offset][x_left].state == self.last_puted_color) and (x_left is not x_offset):
                target_x_left = x_left
                break
            else:
                break

        # コマを置いた右側
        target_x_right = x_offset
        for x_right in range(x_offset + 1, 8):
            if self.pieces[y_offset][x_right].state != self.last_puted_color and self.is_already_put(x_right, y_offset):
                continue
            if (self.pieces[y_offset][x_right].state == self.last_puted_color) and (x_right is not x_offset):
                target_x_right = x_right
                break
            else:
                break

        # 書き換え
        for x in range(x_offset - 1, target_x_left, -1):
            self.pieces[y_offset][x].reverse_piece()

        for x in range(x_offset + 1, target_x_right):
            self.pieces[y_offset][x].reverse_piece()

        ########################################
        # 列
        ########################################
        # コマを置いた上側
        target_y_upper = y_offset
        for y_upper in range(y_offset - 1, -1, -1):
            if self.pieces[y_upper][x_offset].state != self.last_puted_color and self.is_already_put(x_offset, y_upper):
                continue
            if (self.pieces[y_upper][x_offset].state == self.last_puted_color) and (y_upper is not y_offset):
                target_y_upper = y_upper
                break
            else:
                break

        # コマを置いた下側
        target_y_lower = y_offset
        for y_lower in range(y_offset + 1, 8):
            if self.pieces[y_lower][x_offset].state != self.last_puted_color and self.is_already_put(x_offset, y_lower):
                continue
            if (self.pieces[y_lower][x_offset].state == self.last_puted_color) and (y_lower is not y_offset):
                target_y_lower = y_lower
                break
            else:
                break

        # 書き換え
        for y in range(y_offset - 1, target_y_upper, -1):
            self.pieces[y][x_offset].reverse_piece()

        for y in range(y_offset + 1, target_y_lower):
            self.pieces[y][x_offset].reverse_piece()


        ########################################
        # 右上がり斜め
        ########################################
        # コマを置いた左下側
        target_x_left = x_offset
        target_y_lower = y_offset
        for i in range(1, 8):
            x_left = x_offset - i
            y_lower = y_offset + i
            if x_left < 0 or y_lower > 7: #壁にぶつかったら
                break
            if self.pieces[y_lower][x_left].state != self.last_puted_color and self.is_already_put(x_left,y_lower):  # 違う色なら
                continue
            if (self.pieces[y_lower][x_left].state == self.last_puted_color) and (x_left is not x_offset) and (y_lower is not y_offset):
                target_x_left = x_left
                target_y_lower = y_lower
                break
            else:
                break

        # コマを置いた右上側
        target_x_right = x_offset
        target_y_upper = y_offset
        for i in range(1, 8):
            x_right = x_offset + i
            y_upper = y_offset - i
            if x_right > 7 or y_upper < 0:  # 壁にぶつかったら
                break
            if self.pieces[y_upper][x_right].state != self.last_puted_color and self.is_already_put(x_right,y_upper):
                continue
            if (self.pieces[y_upper][x_right].state == self.last_puted_color) and (x_right is not x_offset) and (y_upper is not y_offset):
                target_x_right = x_right
                target_y_upper = y_upper
                break
            else:
                break

        # 書き換え
        for i in range(1, abs(target_x_left - x_offset)):
            x = x_offset - i
            y = y_offset + i
            self.pieces[y][x].reverse_piece()

        for i in range(1, abs(target_x_right - x_offset)):
            x = x_offset + i
            y = y_offset - i
            self.pieces[y][x].reverse_piece()

        ########################################
        # 右下がり斜め
        ########################################
        # コマを置いた左上側
        target_x_left = x_offset
        target_y_upper = y_offset
        for i in range(1, 8):
            x_left = x_offset - i
            y_upper = y_offset - i
            if x_left < 0 or y_upper < 0: #壁にぶつかったら
                break
            if self.pieces[y_upper][x_left].state != self.last_puted_color and self.is_already_put(x_left,y_upper):  # 違う色なら
                continue
            if (self.pieces[y_upper][x_left].state == self.last_puted_color) and (x_left is not x_offset) and (y_upper is not y_offset):
                target_x_left = x_left
                target_y_upper = y_upper
                break
            else:
                break

        # コマを置いた右上側
        target_x_right = x_offset
        target_y_lower = y_offset
        for i in range(1, 8):
            x_right = x_offset + i
            y_lower = y_offset + i
            if x_right > 7 or y_lower > 7:  # 壁にぶつかったら
                break
            if self.pieces[y_lower][x_right].state != self.last_puted_color and self.is_already_put(x_right,y_lower):
                continue
            if (self.pieces[y_lower][x_right].state == self.last_puted_color) and (x_right is not x_offset) and (y_lower is not y_offset):
                target_x_right = x_right
                target_y_lower = y_lower
                break
            else:
                break

        # 書き換え
        for i in range(1, abs(target_x_left - x_offset)):
            x = x_offset - i
            y = y_offset - i
            self.pieces[y][x].reverse_piece()

        for i in range(1, abs(target_x_right - x_offset)):
            x = x_offset + i
            y = y_offset + i
            self.pieces[y][x].reverse_piece()

    def black_is_win(self):
        if self.calc_black_area() > self.calc_white_area():
            return True
        if self.calc_black_area() < self.calc_white_area():
            return False
        return None  # Noneを返せば引き分け


class Player:
    colors = {"black":"black", "white":"white"}
    def __init__(self, name, color):
        self.piece_has = 32  # オセロのコマの所持数
        self.name = name
        self.color = self.colors[color]

    def put_piece(self):
        self.piece_has -= 1


class Game:
    def __init__(self):
        self.p1 = Player("Player1", "white")
        self.p2 = Player("Player2", "black")
        self.board = Board()

    def finish_game(self):
        if self.board.black_is_win() is not None:
            if self.board.black_is_win():
                print("黒が勝ちです。")
            if not self.board.black_is_win():
                print("白が勝ちです。")
        if self.board.black_is_win() is None:
            print("引き分けです。")
        exit()  # これってメモリ解放してくれるん...?

    def turn(self, player):
        while True:
            p_puts = input("{}({})の手番です([x y]で座標を指定してください):".format(player.name, self.board.pieces[0][0].states[player.color]))
            p_puts = p_puts.strip().split(" ")
            if p_puts[0] == 'q':
                self.finish_game()
            px = int(p_puts[0]) - 1
            py = int(p_puts[1]) - 1
            if self.board.is_already_put(px, py):
                print("その場所には既にコマが置かれています。")
                continue
            if (px < 0) or (px >= 8) or (py < 0) or (py >= 8):
                print("範囲外です。")
                continue

            self.board.set_piece_to(px, py, player.color)
            break

    def play_game(self):
        self.board.set_piece_to(3, 3, "black")
        self.board.set_piece_to(4, 4, "black")
        self.board.set_piece_to(3, 4, "white")
        self.board.set_piece_to(4, 3, "white")
        # print(id(self.board.board))
        print(self.board + "\nゲームスタート!\n(qでゲームを中断して終了します)")

        while (self.p1.piece_has != 0) and (self.p1.piece_has != 0):
            self.turn(self.p1)
            self.board.update()
            print(self.board)

            self.turn(self.p2)
            self.board.update()
            print(self.board)

        self.finish_game()

if __name__ == "__main__":
    g = Game()
    g.play_game()