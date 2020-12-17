import random
import string


class GetTestDate:
    def __init__(self):
        self.level_set = [i for i in range(4)]
        self.position_set = [i for i in range(2)]
        self.letter = string.ascii_lowercase
        self.position_num = [i+1 for i in range(2)]

    def get_one_case(self):
        level = random.choice(self.level_set)
        position_num = random.choice(self.position_num)
        position = random.sample(self.position_set, position_num)
        position_sort = sorted(position)
        data_dict = {"level": level, "position": position_sort}
        return data_dict

    def get_player_info(self, n):
        name_list = ["P" + str(i + 1) for i in range(n)]
        play_info_dict = dict()
        for p in name_list:
            play_info_dict[p] = self.get_one_case()
        return play_info_dict


if __name__ == "__main__":
    get_data = GetTestDate()
    infos = get_data.get_player_info(10)
    print(infos)