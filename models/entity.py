class EntityDict:
    def __init__(self):
        self._dict: dict = {}

    def append(self, key: str):
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
        self.append(key1)
        self._dict[key1]['rates']['rates'][key2] = {}
        self._dict[key1]['rates']['rates'][key2]['non-normal'] = rating
        number_ratings = len(self._dict[key1]['rates']['rates'].keys())
        # if rating > self._dict[key1]['rates']['max']:
        #     self._dict[key1]['rates']['max'] = rating
        # if rating < self._dict[key1]['rates']['min']:
        #     self._dict[key1]['rates']['min'] = rating
        if number_ratings == 1:
            self.set_avg(key1, rating)
        else:
            value = (self.get_avg(key1) * (number_ratings - 1) + rating) / number_ratings
            self.set_avg(key1, value)

    def set_normalized_rating(self, key1: str):
        obj = self.get(key1)
        for key in obj['rates']['rates']:
            obj['rates']['rates'][key]['normal'] = self.get_non_normalized_rating(key1, key) - self.get_avg(key1)

    def get_non_normalized_rating(self, key1: str, key2: str):
        return self._dict[key1]['rates']['rates'][key2]['non-normal']

    def get(self, key: str):
        return self._dict[key]

    def get_alias_id(self, item_id: str):
        return self.get(item_id)['alias_id']

    def get_avg(self, key: str):
        return self._dict[key]['rates']['average']

    def get_max(self, key: str):
        return self._dict[key]['rates']['max']

    def get_min(self, key: str):
        return self._dict[key]['rates']['min']

    def set_avg(self, key: str, value: float):
        try:
            self._dict[key]['rates']['average'] = value
        except KeyError:
            self.append(key)
            self._dict[key]['rates']['average'] = value

    def get_rates(self, key: str):
        return self.get(key)['rates']['rates']

    def __call__(self):
        return self._dict
