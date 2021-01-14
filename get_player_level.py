import math
import pandas as pd
import numpy as np
import random
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import minmax_scale
from copy import deepcopy


class GetPlayerLevel:
    def __init__(self):
        self.pw_score_mapping = {'星耀以下': 0.4,
                                 '星耀': 0.6,
                                 '最强车神': 0.8,
                                 "传奇车神": 1}
        self.pw_history_score_mapping = {k: v * 0.4 for k, v in self.pw_score_mapping.items()}
        self.rank_list = ["钻石", "星耀", "最强车神", "传奇车神"]

    def parse_transform(self, origin_df):
        df_ = deepcopy(origin_df)
        df_['胜率'] = np.array([round(float(i), 4) for i in origin_df['胜率']])
        df_['当前排位数据'] = np.array([self.__get_score_by_rank_score(i) for i in origin_df['当前排位数据']])
        df_['历史排位数据'] = np.array([self.__get_score_by_rank_score(i) for i in origin_df['历史排位数据']])
        # print(origin_df)
        return df_

    @staticmethod
    def KMeans(X):
        y_pred = KMeans(n_clusters=3, random_state=9).fit_predict(X)
        print(y_pred)

    @staticmethod
    def PCA(X):
        pca = PCA(n_components=1)
        y = pca.fit_transform(X)
        print(y)

    @staticmethod
    def get_score_by_regular(X, weight):
        w = np.array(weight)
        res_list = []
        for i in range(X.shape[0]):
            res = np.dot(X[i], w)
            res_list.append(res)
        return np.array(res_list)

    @staticmethod
    def data_scaled(X):
        X_scaled = minmax_scale(X)
        # X_scaled = scale.fit_transform(X)
        return X_scaled

    @staticmethod
    def __get_score_by_rank_score(rank_score_string):
        t_list = rank_score_string.split("|")
        if t_list[0] == "星耀":
            score = 75 * 4 + 100 * int(t_list[1]) + int(t_list[2])
        elif t_list[0] == "钻石":
            score = 75 * int(t_list[1]) + int(t_list[2])
        elif t_list[0] in ['最强车神', '传奇车神']:
            score = (75 + 100) * 4 + int(t_list[1])
        else:
            return "bad input"
        return score

    @staticmethod
    def win_rate_function(win_rate):
        win_rate = float(win_rate)
        f1 = win_rate / (1 - win_rate)
        res = math.log(f1)
        if res > 1:
            res = 1
        elif res < 0:
            res = 0
        return round(res, 2)

    def creat_fake_data(self, size):
        data_sub_1 = []
        for i in range(size):
            temp_list = []
            for j in range(2):
                rank = random.choice(self.rank_list)
                rank_stage = random.randint(1, 5)
                rank_score = self.__creat_fake_score_by_rank(rank)
                if rank in ['传奇车神', '最强车神']:
                    level = rank + "|" + str(rank_score)
                else:
                    level = rank + "|" + str(rank_stage) + "|" + str(rank_score)
                temp_list.append(level)
            data_sub_1.append(temp_list)
        data_sub_1 = np.array(data_sub_1)
        id_ = np.array([i + 1 for i in range(size)])
        win_rate = 0.15 * np.random.randn(size) + 0.5
        data_sub_2 = np.column_stack(np.array([id_, win_rate]))
        creat_data = np.hstack((data_sub_2, data_sub_1))
        df = pd.DataFrame(creat_data, columns=['id', '胜率', '当前排位数据', '历史排位数据'])
        return df

    @staticmethod
    def __creat_fake_score_by_rank(rank):
        if rank == '钻石':
            score = random.randint(1, 74)
        elif rank == "星耀":
            score = random.randint(1, 99)
        elif rank == '最强车神':
            score = random.randint(1, 299)
        elif rank == '传奇车神':
            score = random.randint(300, 600)
        else:
            return "wrong input"
        return score


if __name__ == "__main__":
    test_date = {"game_rank": "cqcs",
                 "highest_game_rank_history": 'cqcs',
                 "win_rate": 0.62}
    pl = GetPlayerLevel()
    ori_df = pl.creat_fake_data(10)
    print(ori_df)
    df = pl.parse_transform(ori_df)
    data_x = df.iloc[:, 1:].values
    data_x_scaled = pl.data_scaled(data_x)
    score_ = pl.get_score_by_regular(data_x_scaled, [0.5, 0.3, 0.2])
    print(score_)
    ori_df['得分'] = score_
    print(ori_df)
