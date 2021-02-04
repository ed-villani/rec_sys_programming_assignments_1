import numpy as np
from data_readers.rec_sys_data import RecSysData
from models.item import ItemDict
from models.user import UserDict


class Targets(RecSysData):
    def __init__(self, file_path: str):
        super(Targets, self).__init__(file_path)
        self._solution = np.zeros(len(self.data.index))

    @property
    def solution(self):
        return self._solution

    def to_csv(self, out_path):
        self.data["Prediction"] = self._solution
        self.data.drop(columns=["UserID", "ItemID"], inplace=True)
        self.data.to_csv(out_path, index=False)

    def solve(self, item_dict: ItemDict, user_dict: UserDict, avg: int):
        for index, data in enumerate(np.array(self.data)):
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
                if div != 0:
                    self._solution[index] = item_med + sum(
                        [similarity * user_reviews[user_review]['normal'] for similarity, user_review in
                         zip(item_similarities, user_reviews)]) / div
                else:
                    self._solution[index] = item_med
            elif user in user_dict() and item not in item_dict():
                self._solution[index] = user_dict.get_avg(user)
            elif user not in user_dict() and item in item_dict():
                self._solution[index] = item_dict.get_avg(item)
            else:
                self._solution[index] = avg
