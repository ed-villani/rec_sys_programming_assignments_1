import pandas as pd


class RecSysData:
    def __init__(self, file_path: str):
        self._data = self.read_input_and_split_tuples(file_path)

    @property
    def data(self):
        return self._data

    @staticmethod
    def read_input_and_split_tuples(file_path: str):
        data = pd.read_csv(file_path)
        data_split = data['UserId:ItemId'].str.split(":", n=1, expand=True)
        data['UserID'] = data_split[0]
        data['ItemID'] = data_split[1]
        # data.drop(columns=["UserId:ItemId"], inplace=True)
        return data
