import Chess as ch
import Constants as c
import History as h
import sqlite3

class relation:
    def __init__(self):
        self.chess_type = 0

        self.num_attack = 0
        self.num_guard = 0
        self.num_attacked = 0
        self.num_guarded = 0

        self.attack = [0, 0, 0, 0, 0, 0]
        self.attacked = [0, 0, 0, 0, 0, 0]
        self.guard = [0, 0, 0, 0, 0, 0]
        self.guarded = [0, 0, 0, 0, 0, 0]


class my_game:
    def __init__(self):
        self.board = ch.chess_board()
        self.max_depth = c.max_depth
        self.history_table = h.history_table()
        self.best_move = ch.step()
        self.cnt = 0

    # Alpha-beta pruning, alpha is the most likely lower bound, beta is the smallest possible upper bound
    def alpha_beta(self, depth, alpha, beta):
        who = (self.max_depth - depth) % 2  # That player
        
        # Determine whether the game is over, if it is over, there is no need to search
        if self.is_game_over(who):
            return c.min_val

        # Search to the specified depth
        if depth == 1:
            return self.evaluate(who)
        move_list = self.board.generate_move(who)  # Return to all movable methods

        # Use history table
        for i in range(len(move_list)):
            move_list[i].score = self.history_table.get_history_score(who, move_list[i])
        move_list.sort()  # Sort history board scores for easier pruning
        best_step = move_list[0]
        score_list = []
        for step in move_list:
            temp = self.move_to(step)
            # Because it is one layer to choose the largest and one layer to choose the smallest, 
            # so use the negative sign to achieve
            score = -self.alpha_beta(depth - 1, -beta, -alpha)
            score_list.append(score)
            self.undo_move(step, temp)
            if score > alpha:
                alpha = score
                if depth == self.max_depth:
                    self.best_move = step
                best_step = step
            if alpha >= beta:
                best_step = step
                break

        # Update history table
        if best_step.from_x != -1:
            self.history_table.add_history_score(who, best_step, depth)
        return alpha

    def evaluate(self, who):
        self.cnt += 1
        relation_list = self.init_relation_list()
        base_val = [0, 0]
        pos_val = [0, 0]
        mobile_val = [0, 0]
        relation_val = [0, 0]
        for x in range(9):
            for y in range(10):
                now_chess = self.board.board[x][y]
                type = now_chess.chess_type
                if type == 0:
                    continue
                # now = 0 if who else 1
                now = now_chess.belong
                pos = x * 9 + y
                temp_move_list = self.board.get_chess_move(x, y, now, True)
                # Calculate base value
                base_val[now] += c.base_val[type]
                # Calculate location value
                if now == 0:
                    pos_val[now] += c.pos_val[type][pos]
                else:
                    pos_val[now] += c.pos_val[type][89 - pos]
                # Computer Mobility Value, Record Relationship Information
                for item in temp_move_list:
                    temp_chess = self.board.board[item.to_x][item.to_y]  # Pawn at destination

                    if temp_chess.chess_type == c.invalid:  # If empty, then add mobility value
                        mobile_val[now] += c.mobile_val[type]
                        continue
                    elif temp_chess.belong != now:
                        # If you can eat the opponent's general, then you win
                        if temp_chess.chess_type == c.general:
                            if temp_chess.belong != who:
                                return c.max_val
                            # If not, then it is equivalent to being a general, and the opponent will lose points
                            else:
                                relation_val[1 - now] -= 20
                                continue
                        # Record who was attacked
                        relation_list[x][y].attack[relation_list[x][y].num_attack] = temp_chess.chess_type
                        relation_list[x][y].num_attack += 1
                        relation_list[item.to_x][item.to_y].chess_type = temp_chess.chess_type
                        relation_list[item.to_x][item.to_y].attacked[
                            relation_list[item.to_x][item.to_y].num_attacked] = type
                        relation_list[item.to_x][item.to_y].num_attacked += 1
                    elif temp_chess.belong == now:
                        # There is no point in protecting yourself, just skip it
                        if temp_chess.chess_type == c.general:
                            continue
                        # Record relationship information
                        relation_list[x][y].guard[relation_list[x][y].num_guard] = temp_chess
                        relation_list[x][y].num_guard += 1
                        relation_list[item.to_x][item.to_y].chess_type = temp_chess.chess_type
                        relation_list[item.to_x][item.to_y].guarded[relation_list[item.to_x][item.to_y].num_guarded] = type
                        relation_list[item.to_x][item.to_y].num_guarded += 1
        for x in range(9):
            for y in range(10):
                num_attacked = relation_list[x][y].num_attacked
                num_guarded = relation_list[x][y].num_guarded
                now_chess = self.board.board[x][y]
                type = now_chess.chess_type
                now = now_chess.belong
                unit_val = c.base_val[now_chess.chess_type] >> 3
                sum_attack = 0  # Attacked total
                sum_guard = 0
                min_attack = 999  # Minimal attacker
                max_attack = 0  # Biggest attacker
                max_guard = 0
                flag = 999
                if type == c.invalid:
                    continue
                # Count the attacking side's sub-power
                for i in range(num_attacked):
                    temp = c.base_val[relation_list[x][y].attacked[i]]
                    flag = min(flag, min(temp, c.base_val[type]))
                    min_attack = min(min_attack, temp)
                    max_attack = max(max_attack, temp)
                    sum_attack += temp
                # Count the defender's pieces
                for i in range(num_guarded):
                    temp = c.base_val[relation_list[x][y].guarded[i]]
                    max_guard = max(max_guard, temp)
                    sum_guard += temp
                if num_attacked == 0:
                    relation_val[now] += 5 * relation_list[x][y].num_guarded
                else:
                    muti_val = 5 if who != now else 1
                    if num_guarded == 0:  # Ưithout protection
                        relation_val[now] -= muti_val * unit_val
                    else:  # If protected
                        # If the attacker's sub-power is smaller than the attacked's sub-power, 
                        # the opponent will be willing to change the sub-power
                        if flag != 999: 
                            relation_val[now] -= muti_val * unit_val
                            relation_val[1 - now] -= muti_val * (flag >> 3)
                        # If it is two-for-one, and the smallest sub-force is less than the sum of the attacked sub-force 
                        # and the protector’s sub-force, the opponent may exchange one for two sub-forces
                        elif num_guarded == 1 and num_attacked > 1 and min_attack < c.base_val[type] + sum_guard:
                            relation_val[now] -= muti_val * unit_val
                            relation_val[now] -= muti_val * (sum_guard >> 3)
                            relation_val[1 - now] -= muti_val * (flag >> 3)
                        # If it is three for two and the sum of the attacker's sub-power is smaller than the sum of 
                        # the attacker's sub-power and the protector's sub-power, the opponent may exchange two sub-powers 
                        # for three sub-powers
                        elif num_guarded == 2 and num_attacked == 3 and sum_attack - max_attack < c.base_val[type] + sum_guard:
                            relation_val[now] -= muti_val * unit_val
                            relation_val[now] -= muti_val * (sum_guard >> 3)
                            relation_val[1 - now] -= muti_val * ((sum_attack - max_attack) >> 3)
                        # If n is replaced by n, the number of attackers and protectors is the same, 
                        # and the attacker's sub-power is less than the sum of the attacked sub-power and the protector's sub-power, 
                        # minus the largest sub-power in the protector, then the opponent may exchange n sub-power for n sub-power
                        elif num_guarded == num_attacked and sum_attack < c.base_val[now_chess.chess_type] + sum_guard - max_guard:
                            relation_val[now] -= muti_val * unit_val
                            relation_val[now] -= muti_val * ((sum_guard - max_guard) >> 3)
                            relation_val[1 - now] -= sum_attack >> 3
        my_max_val = base_val[0] + pos_val[0] + mobile_val[0] + relation_val[0]
        my_min_val = base_val[1] + pos_val[1] + mobile_val[1] + relation_val[1]
        if who == 0:
            return my_max_val - my_min_val
        else:
            return my_min_val - my_max_val

    def init_relation_list(self):
        res_list = []
        for i in range(9):
            res_list.append([])
            for j in range(10):
                res_list[i].append(relation())
        return res_list

    def init_lib(self):
        conn = sqlite3.connect("./init_lib/chess.db")
        cursor = conn.cursor()
        sql = "select * from chess"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        print(type(result))
        conn.close()

    # Determine if the game is over
    def is_game_over(self, who):
        for i in range(9):
            for j in range(10):
                if self.board.board[i][j].chess_type == c.general:
                    if self.board.board[i][j].belong == who:
                        return False
        return True

    # Move the pawn
    def move_to(self, step, flag = False):
        belong = self.board.board[step.to_x][step.to_y].belong
        chess_type = self.board.board[step.to_x][step.to_y].chess_type
        temp = ch.chess(belong, chess_type)
        self.board.board[step.to_x][step.to_y].chess_type = self.board.board[step.from_x][step.from_y].chess_type
    
        self.board.board[step.to_x][step.to_y].belong = self.board.board[step.from_x][step.from_y].belong
        self.board.board[step.from_x][step.from_y].chess_type = c.invalid
        self.board.board[step.from_x][step.from_y].belong = -1
        return temp

    # Recovery pawn
    def undo_move(self, step, chess):
        self.board.board[step.from_x][step.from_y].belong = self.board.board[step.to_x][step.to_y].belong
        self.board.board[step.from_x][step.from_y].chess_type = self.board.board[step.to_x][step.to_y].chess_type
        self.board.board[step.to_x][step.to_y].belong = chess.belong
        self.board.board[step.to_x][step.to_y].chess_type = chess.chess_type

if __name__ == "__main__":
    game = my_game()
    while(True):
        from_x = int(input())
        from_y = int(input())
        to_x = int(input())
        to_y = int(input())
        s = ch.step(from_x, from_y, to_x, to_y)

        game.alpha_beta(game.max_depth, c.min_val, c.max_val)
        print(game.best_move)
        game.move_to(game.best_move)
    game.move_to(s)