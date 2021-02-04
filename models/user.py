from models.entity import EntityDict


class UserDict(EntityDict):
    def set_normalized_rating(self, user_id: str):
        super(UserDict, self).set_normalized_rating(user_id)

    def get_non_normalized_rating(self, user_id: str, item_id: str):
        return super(UserDict, self).get_non_normalized_rating(user_id, item_id)

    def add_rating(self, user_id: str, item_id: str, rating: int):
        super(UserDict, self).add_rating(user_id, item_id, rating)