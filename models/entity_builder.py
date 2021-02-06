import numpy as np

from data_readers.ratings import Ratings
from models.item import ItemDict
from models.user import UserDict


class EntityBuilder:
    class _SimilarityMatrixBuilder:
        def __new__(cls, data: Ratings, item_dict: ItemDict, user_dict: UserDict):
            """

            Build a similarity matrix

            :param data: rates information
            :param item_dict: dict of items to get the alisar from
            :param user_dict: dict of user to get the alias from and the avg
            """
            n_users = len(data.get_user_ids())
            n_items = len(data.get_item_ids())
            cls._m = np.zeros((n_users, n_items), dtype=np.float32)
            cls._initialize_matrix(cls, data, item_dict, user_dict)

            return cls._cosine_similarity(cls)

        def _initialize_matrix(self, data: Ratings, item_dict: ItemDict, user_dict: UserDict):
            """

            Initialize a matrix that contains all rates

            :param data: rates information
            :param item_dict: dict of items to get the alisar from
            :param user_dict: dict of user to get the alias from and the avg
            """
            print("Init matrix")
            for data in np.array(data.data):
                item_id = data[4]
                user_id = data[3]
                rating = data[1]
                self._m[user_dict.get_alias_id(user_id)][item_dict.get_alias_id(item_id)] = rating - user_dict.get_avg(
                    user_id)

        def _cosine_similarity(self):
            """

            Generate a cosine similarity matrix

            :return: similarity matrix item v. item
            """
            print("Calculating Similarities")
            norm = (self._m * self._m).sum(0, keepdims=True) ** 0.5
            norm_arr = np.divide(self._m, norm, where=norm != 0)
            similarity_matrix = norm_arr.T @ norm_arr
            return similarity_matrix

    def __new__(cls, data: Ratings) -> (ItemDict, UserDict, float):
        """

        :param data: Ratings class that contains the data to build the dicts
        """
        item_dict, user_dict, avg = _initialize_dicts(data)
        sm = EntityBuilder._SimilarityMatrixBuilder(data, item_dict, user_dict)
        _set_similarities(sm, item_dict)
        return item_dict, user_dict, avg


def _initialize_dicts(data: Ratings) -> (ItemDict, UserDict, float):
    """
    Iter over the rating data to create the user and item dict, also calculate global avg
    :param data: Ratings class that contains the data to build the dicts

    :return newly item and user dict, global avg
    """
    item_dict = ItemDict()
    user_dict = UserDict()
    avg = 0
    print('Initializing Dicts')
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
    return item_dict, user_dict, avg


def _set_similarities(similarity_matrix: np.array, item_dict: ItemDict):
    """

    Iter over all itens in the dict key and set them similarities. We do not need to iter in all
    items, because the matrix is diagonally symmetric. Also ignore zeros values

    :param similarity_matrix:
    :param item_dict:
    """
    print('Putting Similarities in Dicts')
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
