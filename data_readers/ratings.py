import numpy as np

from data_readers.rec_sys_data import RecSysData


class Ratings(RecSysData):
    def __init__(self, file_path: str, n: int = None):
        super(Ratings, self).__init__(file_path)
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

    def get_ratings_from_user(self, user_id):
        return self.data[self.data['UserID'] == user_id]
