from models.entity import EntityDict
from models.user import UserDict


class ItemDict(EntityDict):
    def set_normalized_rating(self, item_id: str, user_list: UserDict):
        obj = self.get(item_id)
        for key in obj['rates']['rates']:
            obj['rates']['rates'][key]['normal'] = self.get_non_normalized_rating(item_id, key) - user_list.get_avg(key)

    def get_non_normalized_rating(self, item_id: str, user_id: str):
        return super(ItemDict, self).get_non_normalized_rating(item_id, user_id)

    def add_rating(self, item_id: str, user_id: str, rating: int):
        super(ItemDict, self).add_rating(item_id, user_id, rating)

    def get_similarity(self, item1: str, item2: str):
        if item2 in self.get(item1)['similarities']:
            return self.get(item1)['similarities'][item2]
        elif item1 in self.get(item2)['similarities']:
            return self.get(item2)['similarities'][item1]
