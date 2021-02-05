import pandas as pd

from data_readers.rec_sys_data import RecSysData


class Ratings(RecSysData):
    def __init__(self, file_path: str, n: int = None):
        """

        Initialize the ratings dataset from its path. n selects how many ratings an item
        must have to not be filtered from the list

        :param file_path: path to ratings file
        :param n: minimum number of ratings an item must have
        """
        super(Ratings, self).__init__(file_path)
        if n is not None:
            self._data = self.get_item_with_more_than_n_ratings(n)

    def get_user_ids(self) -> list:
        """

        Returns all unique user's id from the dataset

        :return: list of users ids
        """
        return list(self._data['UserID'].unique())

    def get_item_ids(self) -> list:
        """

        Returns all unique items's id from the dataset

        :return: list of items ids
        """
        return list(self._data['ItemID'].unique())

    def get_item_with_more_than_n_ratings(self, n: int) -> pd.DataFrame:
        """

        Filters all items with less than n ratings from the dataset

        :param n: minimum number of ratings an item must have
        :return: dataset with items with more than n ratings
        """
        aux_data = self.data.groupby(['ItemID']).count()
        item_list = aux_data[aux_data['Prediction'] > n] \
            .sort_values(by='Prediction', ascending=False) \
            .index \
            .tolist()
        return self.data[self.data['ItemID'].isin(item_list)]
