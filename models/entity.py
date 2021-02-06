class EntityDict:
    def __init__(self):
        self._dict: dict = {}

    def append(self, key: str):
        """

        Create a new dict for that key. Set Alias Id, rates, rates avg and similarities

        :param key: key to created
        """
        if key not in self._dict:
            self._dict[key] = {}
            self._dict[key]['alias_id'] = len(self._dict.keys()) - 1
            self._dict[key]['rates'] = {}
            self._dict[key]['rates']['average'] = 0
            # self._dict[key]['rates']['max'] = 0
            # self._dict[key]['rates']['min'] = np.inf
            self._dict[key]['rates']['rates'] = {}
            self._dict[key]['similarities'] = {}

    def add_rating(self, key1: str, key2: str, rating: int):
        """

        Add a new rate for an key on another key, also update the avg rating

        :param key1: Master Key to receive the ratings
        :param key2: For which key that ratings belongs
        :param rating: rate value
        """
        self.append(key1)
        self._dict[key1]['rates']['rates'][key2] = {}
        self._dict[key1]['rates']['rates'][key2]['non-normal'] = rating
        number_ratings = len(self._dict[key1]['rates']['rates'].keys())
        # if rating > self._dict[key1]['rates']['max']:
        #     self._dict[key1]['rates']['max'] = rating
        # if rating < self._dict[key1]['rates']['min']:
        #     self._dict[key1]['rates']['min'] = rating
        if number_ratings == 1:
            self._set_avg(key1, rating)
        else:
            value = (self.get_avg(key1) * (number_ratings - 1) + rating) / number_ratings
            self._set_avg(key1, value)

    def set_normalized_rating(self, key: str):
        """

        Normalize an entity key rates based on its avg

        :param key: key to be normalized
        """
        obj = self.get(key)
        for rate in obj['rates']['rates']:
            obj['rates']['rates'][rate]['normal'] = self.get_non_normalized_rating(key, rate) - self.get_avg(key)

    def get_non_normalized_rating(self, key1: str, key2: str) -> float:
        """

        Get the non-normal rates of an key on another one

        :param key1: Master Key to get the ratings
        :param key2: For which key that ratings belongs
        :return: The normalized value of key1 on key2
        """
        return self._dict[key1]['rates']['rates'][key2]['non-normal']

    def get(self, key: str) -> dict:
        """

        :param key: Key to be returned
        :return: Return the dict of that key
        """
        return self._dict[key]

    def get_alias_id(self, key: str) -> str:
        """

        :param key: Key to be returned
        :return: Return the alias id of that key
        """
        return self.get(key)['alias_id']

    def get_avg(self, key: str) -> float:
        """

        :param key: Key to be returned
        :return: Return the abg rating of that key
        """
        return self._dict[key]['rates']['average']

    def _set_avg(self, key: str, value: float):
        """
        Set the avg rating of that key
        :param value: value to be set
        :param key: Key to have avg set
        """
        try:
            self._dict[key]['rates']['average'] = value
        except KeyError:
            self.append(key)
            self._dict[key]['rates']['average'] = value

    def get_rates(self, key: str) -> dict:
        """

        :param key: Key to get the rates
        :return: Rates of that key
        """
        return self.get(key)['rates']['rates']

    def __call__(self) -> dict:
        """
        :return: The Dict that represent the data
        """
        return self._dict
