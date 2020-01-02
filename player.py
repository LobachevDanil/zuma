import dill


class Player:
    def __init__(self, name, scores=0):
        """
        @type name: str
        @type scores: int
        """
        self.name = name
        self.scores = scores

    def inc_scores(self, length):
        multiplicity = length - 2
        self.scores += multiplicity * length * 100


class ResultTable:
    def __init__(self):
        self._players = []
        self.name = 'scores_table.txt'
        self._download_table()

    def _download_table(self):
        with open('saves/' + self.name, 'rb')as f:
            self._players = dill.load(f)

    def save_table(self):
        self._sort_table()
        with open('saves/' + self.name, 'wb') as f:
            dill.dump(self._players, f)

    def _sort_table(self):
        self._players.sort(key=lambda x: x.scores)

    def get_table(self):
        self._sort_table()
        return self._players
