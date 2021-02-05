import pandas as pd


class RecSysData:
    def __init__(self, file_path: str):
        """

        Initialize an dataset from its path.

        :param file_path: path to ratings file
        """
        self._data: pd.DataFrame = self.read_input_and_split_tuples(file_path)

    @property
    def data(self) -> pd.DataFrame:
        """

        Get the dataset

        :return: the dataset
        """
        return self._data

    @staticmethod
    def read_input_and_split_tuples(file_path: str) -> pd.DataFrame:
        """

        Read the data and splits its column 'UserId:ItemId' in two column

        :param file_path: path to ratings file
        """
        data = pd.read_csv(file_path)
        data_split = data['UserId:ItemId'].str.split(":", n=1, expand=True)
        data['UserID'] = data_split[0]
        data['ItemID'] = data_split[1]
        # data.drop(columns=["UserId:ItemId"], inplace=True)
        return data
