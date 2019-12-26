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
        with open(self.name, 'r', encoding='utf-8')as f:
            for line in f:
                words = line.split('|')
                self._players.append(Player(words[0], int(words[1])))

    def save_table(self):
        self._sort_table()
        with open(self.name, 'w', encoding='utf-8') as f:
            f.writelines(self._players)

    def _sort_table(self):
        self._players.sort(key=lambda x: x.scores)

    def get_table(self):
        self._sort_table()
        return self._players
