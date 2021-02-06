import numpy as np
from models.entity import EntityDict
from models.user import UserDict


class ItemDict(EntityDict):
    def set_normalized_rating(self, item_id: str, user_list: UserDict):
        """

        Normalize an item rates based on the users avg avg

        :param user_list: list of user that have their avg rating
        :param item_id: item to be normalized
        """

        obj = self.get(item_id)
        for key in obj['rates']['rates']:
            obj['rates']['rates'][key]['normal'] = self.get_non_normalized_rating(item_id, key) - user_list.get_avg(key)

    def get_non_normalized_rating(self, item_id: str, user_id: str):
        """

        Get the non-normal rates of an item from an user

        :param item_id: ITem that has the rating
        :param user_id: For which key that ratings belongs
        :return: The normalized value of item_id on user_id
        """
        return super(ItemDict, self).get_non_normalized_rating(item_id, user_id)

    def add_rating(self, item_id: str, user_id: str, rating: int):
        """

        Add a new rate for an Item from an user, also update the avg rating

        :param user_id: User which ratings belongs
        :param item_id: Item to receive the ratings
        :param rating: rate value
        """
        super(ItemDict, self).add_rating(item_id, user_id, rating)

    def get_similarity(self, item: str, user_rates: dict) -> (float, np.ndarray):
        """

        Get the similarities from item

        :param user_rates: dict of all rates
        :param item: Item to get similariies
        :return: Similarities from item
        """
        all_sm = self.sm[self.get_alias_id(item)]
        return np.sum(np.abs(all_sm)), all_sm[[self.get_alias_id(item_user) for item_user in user_rates]]
