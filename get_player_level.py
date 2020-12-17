import math


class GetPlayerLevel:
    def __init__(self):
        self.pw_score_mapping = {"cqcs": 1,
                                 'zqcs': 0.8,
                                 'xy': 0.6,
                                 '_xy': 0.4}
        self.pw_history_score_mapping = {k: v * 0.4 for k, v in self.pw_score_mapping.items()}

    @staticmethod
    def win_rate_function(win_rate):
        f1 = win_rate / (1 - win_rate)
        res = math.log(f1)
        if res > 1:
            res = 1
        elif res < 0:
            res = 0
        return round(res, 2)

    def get_one_player_score(self, player_info):
        score_pw = self.pw_score_mapping[player_info["game_rank"]]
        score_pw_his = self.pw_history_score_mapping[player_info["highest_game_rank_history"]]
        score_win_rate = self.win_rate_function(player_info["win_rate"])
        score = score_pw + score_pw_his + score_win_rate
        return score


if __name__ == "__main__":
    test_date = {"game_rank": "cqcs",
                 "highest_game_rank_history": 'cqcs',
                 "win_rate": 0.62}
    pl = GetPlayerLevel()
    print(pl.get_one_player_score(test_date))
