from copy import deepcopy
import random
from init_data_test import GetTestDate


class MatchSystem:
    def __init__(self, player_info):
        self.position_set = [i for i in range(3)]
        self.player_info = player_info

    def get_match_result(self, game_num, max_level_diff=100):
        player_game_num_dict = {player: 0 for player, info in self.player_info.items()}
        while self.not_touch_max_num(player_game_num_dict, game_num):
            # step_1：选出第一支队伍
            player_game_num_sorted = sorted(player_game_num_dict.items(), key=lambda x: x[1])
            first_player, first_play_num = player_game_num_sorted.pop(0)
            cnt_dict = self.get_new_dict_by_value(player_game_num_sorted)
            cnt_dict_sorted = sorted(cnt_dict.items(), key=lambda x: x[0])
            rest_player_list = self.splice_list_in_dict_items(cnt_dict_sorted)
            _, min_cnt_list = cnt_dict_sorted[0]
            second_player = random.choice(min_cnt_list)
            rest_player_list.remove(second_player)
            random.shuffle(rest_player_list)

            team_position = self.player_info[first_player]["position"]
            team_position.extend(self.player_info[second_player]["position"])
            for player in rest_player_list:
                team_position.extend(self.player_info[player]["position"])
                team_position_set = set(team_position)
                if 0 in team_position_set and 1 in team_position_set:
                    third_player = player
                    rest_player_list.remove(third_player)
                    break

            player_game_num_dict[first_player] += 1
            player_game_num_dict[second_player] += 1
            player_game_num_dict[third_player] += 1
            team_level = self.player_info[first_player]["level"] + self.player_info[second_player]["level"] + \
                         self.player_info[third_player]["level"]

            # step_2：根据第一支队伍选出第二支队伍
            rest_player_dict = {p: player_game_num_dict[p] for p in rest_player_list}
            # # 重复选择第一支队伍的逻辑
            rest_player_dict_sorted = sorted(rest_player_dict.items(), key=lambda x: x[1])
            fourth_player, fourth_player_num = rest_player_dict_sorted.pop(0)
            cnt_dict_ = self.get_new_dict_by_value(rest_player_dict_sorted)
            cnt_dict_sorted_ = sorted(cnt_dict_.items(), key=lambda x: x[0])
            rest_player_list_ = self.splice_list_in_dict_items(cnt_dict_sorted_)
            _, min_cnt_list_ = cnt_dict_sorted_[0]
            fifth_player = random.choice(min_cnt_list_)
            rest_player_list_.remove(fifth_player)
            random.shuffle(rest_player_list_)

            other_team_position = self.player_info[fourth_player]["position"]
            other_team_position.extend(self.player_info[fifth_player]["position"])
            other_team_position_copy = deepcopy(other_team_position)
            other_team_level = self.player_info[fourth_player]["level"] + self.player_info[fifth_player]["level"]
            sixth_player_list = []
            position_rest = []
            for player in rest_player_list_:
                other_team_position_copy.extend(self.player_info[player]["position"])
                other_team_position_copy_set = set(other_team_position)
                if 0 in other_team_position_copy_set and 1 in other_team_position_copy_set:
                    position_rest.append(player)
                    if team_level - other_team_level < max_level_diff:
                        sixth_player_list.append(player)
                        rest_player_list_.remove(player)
                        break

            if not sixth_player_list:
                # if not position_rest
                level_dict = {p: self.player_info[p]["level"] for p in position_rest}
                level_list_sorted = sorted(level_dict, key=lambda x: x[1])
                min_level_player, min_level = level_list_sorted[0]
                max_level_player, max_level = level_list_sorted[len(level_list_sorted) - 1]
                if other_team_level > team_level:
                    sixth_player = min_level_player
                else:
                    sixth_player = max_level_player
                sixth_player = sixth_player
            else:
                sixth_player = sixth_player_list[0]

            print([first_player, second_player, third_player],
                  [fourth_player, fifth_player, sixth_player])
            player_game_num_dict[fourth_player] += 1
            player_game_num_dict[fifth_player] += 1
            player_game_num_dict[sixth_player] += 1

        print(player_game_num_dict)

    @staticmethod
    def del_max_num_player(player_game_num_dict, max_num):
        copy_dict = deepcopy(player_game_num_dict)
        for player, num in player_game_num_dict.items():
            if num >= max_num:
                del copy_dict[player]
        return copy_dict

    @staticmethod
    def not_touch_max_num(player_game_num_dict, max_num):
        for p, num in player_game_num_dict.items():
            if num < max_num:
                return True
        return False

    @staticmethod
    def get_new_dict_by_value(count_dict_items):
        new_count_dict = {}
        for k, cnt in count_dict_items:
            k_ = str(k)
            cnt_ = str(cnt)
            if cnt_ not in new_count_dict:
                new_count_dict[cnt_] = [k_]
            else:
                new_count_dict[cnt_].append(k_)
        return new_count_dict

    @staticmethod
    def splice_list_in_dict_items(dict_items):
        res_list = []
        for k, v_list in dict_items:
            res_list.extend(v_list)
        return res_list


if __name__ == "__main__":
    get_data = GetTestDate()
    infos = get_data.get_player_info(24)
    print(infos)
    print("**" * 30)
    ms = MatchSystem(infos)
    ms.get_match_result(8)
