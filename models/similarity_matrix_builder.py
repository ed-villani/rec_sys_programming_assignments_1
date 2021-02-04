import numpy as np

from data_readers.ratings import Ratings
from models.item import ItemDict
from models.user import UserDict


class SimilarityMatrixBuilder:
    def __new__(cls, data: Ratings, item_dict: ItemDict, user_dict: UserDict):
        n_users = len(data.get_user_ids())
        n_items = len(data.get_item_ids())
        cls._m = np.zeros((n_users, n_items), dtype=np.float32)
        cls._initialize_matrix(cls, data, item_dict, user_dict)

        return cls._cosine_similarity(cls)

    def _initialize_matrix(self, data: Ratings, item_dict: ItemDict, user_dict: UserDict):
        for data in np.array(data.data):
            item_id = data[4]
            user_id = data[3]
            rating = data[1]
            self._m[user_dict.get_alias_id(user_id)][item_dict.get_alias_id(item_id)] = rating - user_dict.get_avg(
                user_id)

    def _cosine_similarity(self):
        norm = (self._m * self._m).sum(0, keepdims=True) ** 0.5
        norm_arr = np.divide(self._m, norm, where=norm != 0)
        similarity_matrix = norm_arr.T @ norm_arr
        return similarity_matrix
