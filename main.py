import math

import numpy as np
import pandas as pd
from tqdm import tqdm


class RecSysData:
    def __init__(self, input):
        self._data = self.read_input_and_split_tuples(input)

    @property
    def data(self):
        return self._data

    @staticmethod
    def read_input_and_split_tuples(input):
        data = pd.read_csv(input)
        data_split = data['UserId:ItemId'].str.split(":", n=1, expand=True)
        data['UserID'] = data_split[0]
        data['ItemID'] = data_split[1]
        data.drop(columns=["UserId:ItemId"], inplace=True)
        return data


class Targets(RecSysData):
    pass


class Ratings(RecSysData):
    def __init__(self, input, n=None):
        super(Ratings, self).__init__(input)
        if n is not None:
            self._data = self.get_item_with_more_than_n_ratings(n)

    def get_item_index(self, item_id):
        return np.int8(np.where(self.get_item_ids() == item_id)[0][0])

    def get_user_index(self, user_id):
        return np.int8(np.where(self.get_user_ids() == user_id)[0][0])

    def get_user_ids(self):
        return list(self._data['UserID'].unique())

    def get_item_ids(self):
        return list(self._data['ItemID'].unique())

    def get_item_with_more_than_n_ratings(self, n):
        aux_data = self.data.groupby(['ItemID']).count()
        item_list = aux_data[aux_data['Prediction'] > n] \
            .sort_values(by='Prediction', ascending=False) \
            .index \
            .tolist()
        return self.data[self.data['ItemID'].isin(item_list)]

    def get_ratings_from_item(self, item_id):
        return self.data[self.data['ItemID'] == item_id]

    def get_ratings_from_item(self, user_id):
        return self.data[self.data['UserID'] == user_id]

    def compare_items_ratings(self, item1, item2):
        return pd.merge(
            self.get_ratings_from_item(item1),
            self.get_ratings_from_item(item2),
            how='outer',
            on='UserID'
        ).fillna(0)

    def cosine_similarity(self, item1, item2):
        ratings = self.compare_items_ratings(item1, item2)
        dot_prod = np.dot(
            ratings['Prediction_x'],
            ratings['Prediction_y']
        )
        norm_prod = np.linalg.norm(ratings['Prediction_x']) * np.linalg.norm(ratings['Prediction_y'])
        return dot_prod / norm_prod

    def generate_matrix(self):
        item_list = self.data['ItemID'].unique()
        user_list = self.data['UserID'].unique()
        matrix = pd.DataFrame(0, index=item_list, columns=user_list)
        for index, item in enumerate(item_list):
            print(f'generate_matrix: #{index} item {item}')
            prediction = self.get_ratings_from_item(item)
            y = matrix.T.reset_index()[["index", item]]
            y = y.rename(columns={'index': "UserID"})
            result = pd.merge(
                prediction,
                y,
                how='outer',
                on='UserID'
            ).fillna(0)['Prediction'].tolist()
            l = matrix.T
            l[item] = result
            matrix = l.T
        return matrix


def cosine_dic(dic1, dic2, rate_type='normal'):
    numerator = 0
    dena = 0
    for key1, val1 in dic1.items():
        dic2val2 = dic2.get(key1, 0.0)
        if isinstance(dic2val2, dict):
            dic2val2 = dic2val2[rate_type]
        val1 = val1[rate_type]
        numerator += val1 * dic2val2
        dena += val1 * val1
    denb = 0
    if numerator == 0:
        return 0
    for key2, val2 in dic2.items():
        denb += val2[rate_type] * val2[rate_type]
    try:
        return numerator / math.sqrt(dena * denb)
    except ZeroDivisionError:
        return 0


class EntityDict:
    def __init__(self):
        self._dict: dict = {}

    def append(self, key: str):
        if key not in self._dict:
            self._dict[key] = {}
            self._dict[key]['alias_id'] = len(self._dict.keys()) - 1
            self._dict[key]['rates'] = {}
            self._dict[key]['rates']['average'] = 0
            self._dict[key]['rates']['max'] = 0
            self._dict[key]['rates']['min'] = np.inf
            self._dict[key]['rates']['rates'] = {}
            self._dict[key]['similarities'] = {}

    def add_rating(self, key1: str, key2: str, rating: int):
        self.append(key1)
        self._dict[key1]['rates']['rates'][key2] = {}
        self._dict[key1]['rates']['rates'][key2]['non-normal'] = rating
        number_ratings = len(self._dict[key1]['rates']['rates'].keys())
        if rating > self._dict[key1]['rates']['max']:
            self._dict[key1]['rates']['max'] = rating
        if rating < self._dict[key1]['rates']['min']:
            self._dict[key1]['rates']['min'] = rating
        if number_ratings == 1:
            self.set_avg(key1, rating)
        else:
            value = (self.get_avg(key1) * (number_ratings - 1) + rating) / number_ratings
            self.set_avg(key1, value)

    def set_normalized_rating(self, key1: str):
        obj = self.get(key1)
        for key in obj['rates']['rates']:
            obj['rates']['rates'][key]['normal'] = self.get_non_normalized_rating(key1, key) - self.get_avg(key1)

    def get_non_normalized_rating(self, key1: str, key2: str):
        return self._dict[key1]['rates']['rates'][key2]['non-normal']

    def get(self, key: str):
        return self._dict[key]

    def get_alias_id(self, item_id: str):
        return self.get(item_id)['alias_id']

    def get_avg(self, key: str):
        return self._dict[key]['rates']['average']

    def get_max(self, key: str):
        return self._dict[key]['rates']['max']

    def get_min(self, key: str):
        return self._dict[key]['rates']['min']

    def set_avg(self, key: str, value: float):
        try:
            self._dict[key]['rates']['average'] = value
        except KeyError:
            self.append(key)
            self._dict[key]['rates']['average'] = value

    def get_rates(self, key: str):
        return self.get(key)['rates']['rates']

    def __call__(self):
        return self._dict


class UserDict(EntityDict):
    def set_normalized_rating(self, user_id: str):
        super(UserDict, self).set_normalized_rating(user_id)

    def get_non_normalized_rating(self, user_id: str, item_id: str):
        return super(UserDict, self).get_non_normalized_rating(user_id, item_id)

    def add_rating(self, user_id: str, item_id: str, rating: int):
        super(UserDict, self).add_rating(user_id, item_id, rating)


class ItemDict(EntityDict):
    def set_normalized_rating(self, item_id: str, user_list: UserDict):
        obj = self.get(item_id)
        for key in obj['rates']['rates']:
            obj['rates']['rates'][key]['normal'] = self.get_non_normalized_rating(item_id, key) - user_list.get_avg(key)

    def get_non_normalized_rating(self, item_id: str, user_id: str):
        return super(ItemDict, self).get_non_normalized_rating(item_id, user_id)

    def add_rating(self, item_id: str, user_id: str, rating: int):
        super(ItemDict, self).add_rating(item_id, user_id, rating)

    def _set_similarity(self, item1: str, item2: str):
        similarity = cosine_dic(self.get_rates(item1), self.get_rates(item2))
        self.get(item1)['similarities'][item2] = similarity
        self.get(item2)['similarities'][item1] = similarity
        return similarity

    def get_similarity(self, item1: str, item2: str):
        if item2 in self.get(item1)['similarities']:
            return self.get(item1)['similarities'][item2]
        elif item1 in self.get(item2)['similarities']:
            return self.get(item2)['similarities'][item1]
        return self._set_similarity(item1, item2)


def main():
    ratings = Ratings("inputs/ratings.csv", 4)

    item_dict = ItemDict()
    user_dict = UserDict()
    avg = 0
    for data in tqdm(np.array(ratings.data)):
        item_id = data[3]
        user_id = data[2]
        rating = data[0]

        item_dict.add_rating(item_id, user_id, rating)
        user_dict.add_rating(user_id, item_id, rating)
        avg = avg + rating
    avg = avg / len(ratings.data)

    for item in tqdm(item_dict()):
        item_dict.set_normalized_rating(item, user_dict)
    for user in tqdm(user_dict()):
        user_dict.set_normalized_rating(user)

    arr = np.zeros((len(ratings.get_item_ids()), len(ratings.get_user_ids())), dtype=np.float32)
    for data in tqdm(np.array(ratings.data)):
        item_id = data[3]
        user_id = data[2]
        rating = data[0]
        arr[item_dict.get_alias_id(item_id)][user_dict.get_alias_id(user_id)] = rating - user_dict.get_avg(user_id)

    arr = arr.T

    norm = (arr * arr).sum(0, keepdims=True) ** 0.5
    norm = np.divide(arr, norm, out=np.zeros_like(arr), where=norm != 0)
    cos = norm.T @ norm

    for item1 in tqdm(item_dict()):
        itemA = item_dict()[item1]
        if 'similarities' not in itemA:
            itemA['similarities'] = {}
        for item2 in item_dict():
            if item1 == item2:
                break
            value = cos[item_dict.get_alias_id(item2)][item_dict.get_alias_id(item1)]
            if value == 0:
                break
            itemA['similarities'][item2] = value

    raw = pd.read_csv("inputs/targets.csv")
    raw[["user", "item"]] = raw["UserId:ItemId"].str.split(":", 1, expand=True)
    ratings = np.zeros(len(raw.index))
    index = 0

    for data in tqdm(np.array(raw)):
        user = data[1]
        item = data[2]
        if user in user_dict() and item in item_dict():
            user_reviews = user_dict.get_rates(user)
            item_similarities = [
                item_dict()[item]['similarities'][item_user] if item_user in item_dict()[item]['similarities']
                else 0
                for item_user in user_reviews
            ]
            item_med = item_dict.get_avg(item)
            div = sum(
                abs(similarity) for similarity in item_similarities
            )
            if div:
                ratings[index] = item_med + sum(
                    [similarity * user_reviews[user_review]['normal'] for similarity, user_review in
                     zip(item_similarities, user_reviews)]) / div
            else:
                ratings[index] = item_med
        elif user in user_dict() and item not in item_dict():
            ratings[index] = user_dict.get_avg(user)
        elif user not in user_dict() and item in item_dict():
            ratings[index] = item_dict.get_avg(item)
        else:
            ratings[index] = avg
        index = index + 1

    raw["Prediction"] = ratings
    raw.drop(columns=["user", "item"]).to_csv("output.csv", index=False)


if __name__ == '__main__':
    main()
