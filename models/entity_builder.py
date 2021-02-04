import numpy as np

from data_readers.ratings import Ratings
from models.item import ItemDict
from models.similarity_matrix_builder import SimilarityMatrixBuilder
from models.user import UserDict


class EntityBuilder:
    def __new__(cls, data: Ratings):
        avg, item_dict, user_dict = EntityBuilder._initialize_dicts(data)
        sm = SimilarityMatrixBuilder(data, item_dict, user_dict)
        cls._set_similarities(sm, item_dict)
        return item_dict, user_dict, avg

    @staticmethod
    def _initialize_dicts(data: Ratings):
        item_dict = ItemDict()
        user_dict = UserDict()
        avg = 0
        for row in np.array(data.data):
            item_id = row[4]
            user_id = row[3]
            rating = row[1]

            item_dict.add_rating(item_id, user_id, rating)
            user_dict.add_rating(user_id, item_id, rating)
            avg = avg + rating
        avg = avg / len(data.data)
        for item in item_dict():
            item_dict.set_normalized_rating(item, user_dict)
        for user in user_dict():
            user_dict.set_normalized_rating(user)
        return avg, item_dict, user_dict

    @staticmethod
    def _set_similarities(similarity_matrix: np.array, item_dict: ItemDict):
        for item1 in item_dict():
            itemA = item_dict()[item1]
            if 'similarities' not in itemA:
                itemA['similarities'] = {}
            for item2 in item_dict():
                if item1 == item2:
                    break
                value = similarity_matrix[item_dict.get_alias_id(item2)][item_dict.get_alias_id(item1)]
                if value == 0:
                    break
                itemA['similarities'][item2] = value
                itemB = item_dict()[item2]
                itemB['similarities'][item1] = value
