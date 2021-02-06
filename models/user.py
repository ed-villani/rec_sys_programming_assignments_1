from models.entity import EntityDict


class UserDict(EntityDict):
    def set_normalized_rating(self, user_id: str):
        """

        Normalize an item rates based on the users avg avg

        :param user_id: item to be normalized
        """
        super(UserDict, self).set_normalized_rating(user_id)

    def get_non_normalized_rating(self, user_id: str, item_id: str):
        """

        Get the non-normal rates of an item from an user

        :param user_id: User that has the rating
        :param item_id: For which key that ratings belongs
        :return: The normalized value of user_id on item_id
        """
        return super(UserDict, self).get_non_normalized_rating(user_id, item_id)

    def add_rating(self, user_id: str, item_id: str, rating: int):
        """

        Add a new rate for an Item from an user, also update the avg rating

        :param item_id: Item which ratings belongs
        :param user_id: User to receive the ratings
        :param rating: rate value
        """
        super(UserDict, self).add_rating(user_id, item_id, rating)
