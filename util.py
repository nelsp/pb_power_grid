import json

config = json.loads(open('config.json').read())

europe = [(('red', 'Lisboa'), ('red', 'Madrid'), 13), (('red', 'Madrid'), ('red', 'Bordeaux'), 16), (('red', 'Barcelona'), ('red', 'Marseille'), 11), (('red', 'Barcelona'), ('red', 'Madrid'), 14),
          (('red', 'Barcelona'), ('red', 'Bordeaux'), 15), (('red', 'Marseille'), ('red', 'Bordeaux'), 12), (('red', 'Bordeaux'), ('red', 'Paris'), 12), (('red', 'Marseille'), ('red', 'Lyon'), 8),
          (('red', 'Bordeaux'), ('red', 'Lyon'), 12), (('purple', 'London'), ('red', 'Paris'), 16), (('red', 'Paris'), ('red', 'Lyon'), 11), (('red', 'Paris'), ('purple', 'Rhein-Ruhr'), 10),
          (('red', 'Paris'), ('purple', 'Rhein-Ruhr'), 10), (('red', 'Paris'), ('purple', 'Vlaanderen'), 7), (('purple', 'Randstad'), ('purple', 'London'), 18), (('purple', 'Rhein-Ruhr'), ('purple', 'Vlaanderen'), 4),
          (('purple', 'Vlaanderen'), ('purple', 'London'), 15), (('purple', 'London'), ('purple', 'Birmingham'), 4), (('purple', 'Birmingham'), ('purple', 'Glasgow'), 13), (('purple', 'Birmingham'), ('purple', 'Dublin'), 15),
          (('purple', 'Dublin'), ('purple', 'Glasgow'), 17), (('purple', 'Randstad'), ('purple', 'Vlaanderen'), 4), (('red', 'Paris'), ('brown', 'Stuttgart'), 14), (('purple', 'Randstad'), ('brown', 'Bremen'), 8),
          (('purple', 'Vlaanderen'), ('brown', 'Bremen'), 10), (('purple', 'Vlaanderen'), ('brown', 'Rhein-Main'), 6), (('purple', 'Rhein-Ruhr'), ('brown', 'Rhein-Main'), 3),
          (('purple', 'Rhein-Ruhr'), ('brown', 'Stuttgart'), 5), (('brown', 'Rhein-Main'), ('brown', 'Stuttgart'), 3), (('brown', 'Rhein-Main'), ('brown', 'Berlin'), 10), (('brown', 'Rhein-Main'), ('brown', 'Praha'), 10),
          (('brown', 'Rhein-Main'), ('brown', 'Munchen'), 6), (('brown', 'Stuttgart'), ('brown', 'Munchen'), 4), (('brown', 'Berlin'), ('brown', 'Bremen'), 6), (('brwon', 'Praha'), ('brown', 'Munchen'), 8),
          (('brown', 'Praha'), ('brown', 'Katowice'), 8), (('brown', 'Praha'), ('brown', 'Berlin'), 7), (('blue', 'Beograd'), ('blue', 'Tirane'), 15), (('blue', 'Beograd'), ('blue', 'Sofia'), 11),
          (('blue', 'Sofia'), ('blue', 'Tirane'), 13), (('blue', 'Sofia'), ('blue', 'Istanbul'), 13), (('blue', 'Sofia'), ('blue', 'Athina'), 17), (('blue', 'Tirane'), ('blue', 'Athina'), 16),
          (('blue', 'Istanbul'), ('blue', 'Izmir'), 8), (('blue', 'Istanbul'), ('blue', 'Ankara'), 9), (('blue', 'Izmir'), ('blue', 'Ankara'), 10), (('blue', 'Beograd'), ('green', 'Bucuresti'), 12),
          (('blue', 'Sofia'), ('green', 'Bucuresti'), 9), (('blue', 'Istanbul'), ('green', 'Bucuresti'), 13), (('blue', 'Beograd'), ('yellow', 'Budapest'), 10), (('brown', 'Rhein-Main'), ('brown', 'Stuttgart'), 3),
          (('brown', 'Rhein-Main'), ('brown', 'Bremen'), 9), (('brown', 'Rhein-Main'), ('brown', 'Berlin'), 10), (('brown', 'Rhein-Main'), ('brown', 'Praha'), 10), (('brown', 'Rhein-Main'), ('brown', 'Munchen'), 6),
          (('brown', 'Rhein-Main'), ('purple', 'Rhein-Ruhr'), 3), (('brown', 'Rhein-Main'), ('purple', 'Vlaanderen'), 6), (('brown', 'Bremen'), ('purple', 'Vlaanderen'), 10), (('green', 'Kyjiv'), ('brown', 'Katowice'), 18),
          (('green', 'Warszawa'), ('brown', 'Katowice'), 5), (('green', 'Warszawa'), ('brown', 'Praha'), 11), (('green', 'Warszawa'), ('brown', 'Berlin'), 11), (('green', 'Kyjiv'), ('green', 'Warszawa'), 14),
          (('green', 'Kyjiv'), ('green', 'Minsk'), 10), (('green', 'Kyjiv'), ('green', 'Kharkiv'), 9), (('green', 'Kyjiv'), ('green', 'Odessa'), 9), (('green', 'Kharkiv'), ('green', 'Odessa'), 13),
          (('green', 'Kharkiv'), ('green', 'Moskwa'), 15), (('green', 'Warszawa'), ('green', 'Minsk'), 10), (('green', 'Warszawa'), ('orange', 'Kobenhavn'), 25), (('green', 'Kyjiv'), ('yellow', 'Budapest'), 21),
          (('orange', 'Kobenhavn'), ('brown', 'Bremen'), 12), (('orange', 'Kobenhavn'), ('brown', 'Berlin'), 15), (('orange', 'Riga'), ('green', 'Warszawa'), 12), (('orange', 'Riga'), ('green', 'Minsk'), 8),
          (('orange', 'Riga'), ('green', 'Moskwa'), 18), (('orange', 'Kobenhavn'), ('green', 'Warszawa'), 25), (('orange', 'Riga'), ('orange', 'Sankt-Peterburg'), 13), (('orange', 'Riga'), ('orange', 'Tallinn'), 7),
          (('orange', 'Kobenhavn'), ('orange', 'Stockholm'), 18), (('orange', 'Kobenhavn'), ('orange', 'Oslo'), 17), (('orange', 'Stockholm'), ('orange', 'Oslo'), 13), (('orange', 'Stockholm'), ('orange', 'Helsinki'), 21),
          (('orange', 'Sankt-Peterburg'), ('orange', 'Tallinn'), 9), (('orange', 'Sankt-Peterburg'), ('orange', 'Helsinki'), 11), (('purple', 'Randstad'), ('brown', 'Bremen'), 8), (('yellow', 'Napoli'), ('blue', 'Tirane'), 25),
          (('yellow', 'Napoli'), ('blue', 'Beograd'), 18), (('yellow', 'Zagreb'), ('blue', 'Beograd'), 9), (('yellow', 'Milano'), ('brown', 'Munchen'), 16), (('yellow', 'Zurich'), ('brown', 'Stuttgart'), 5),
          (('yellow', 'Zurich'), ('brown', 'Munchen'), 8), (('yellow', 'Zagreb'), ('brown', 'Munchen'), 14), (('yellow', 'Milano'), ('red', 'Marseille'), 13), (('yellow', 'Milano'), ('red', 'Lyon'), 11),
          (('yellow', 'Zurich'), ('red', 'Lyon'), 14), (('yellow', 'Zurich'), ('red', 'Paris'), 14), (('yellow', 'Milano'), ('yellow', 'Zurich'), 11), (('yellow', 'Milano'), ('yellow', 'Roma'), 19),
          (('yellow', 'Milano'), ('yellow', 'Zagreb'), 17), (('yellow', 'Napoli'), ('yellow', 'Roma'), 7), (('yellow', 'Zagreb'), ('yellow', 'Wien'), 8), (('yellow', 'Zagreb'), ('yellow', 'Budapest'), 7),
          (('yellow', 'Budapest'), ('brown', 'Katowice'), 11), (('yellow', 'Budapest'), ('green', 'Odessa'), 25), (('yellow', 'Budapest'), ('green', 'Bucuresti'), 16), (('yellow', 'Budapest'), ('yellow', 'Wien'), 5),
          (('brown', 'Berlin'), ('brown', 'Praha'), 7), (('brown', 'Bremen'), ('brown', 'Berlin'), 6), (('brown', 'Katowice'), ('yellow', 'Budapest'), 11),
          (('brown', 'Katowice'), ('brown', 'Praha'), 8), (('brown', 'Katowice'), ('yellow', 'Wien'), 8), (('brown', 'Munchen'), ('brown', 'Stuttgart'), 4),
          (('brown', 'Praha'), ('yellow', 'Wien'), 7), (('brown', 'Stuttgart'), ('brown', 'Munchen'), 4), (('brown', 'Stuttgart'), ('purple', 'Rhein-Ruhr'), 5),
          (('brown', 'Stuttgart'), ('red', 'Paris'), 14), (('green', 'Bucuresti'), ('yellow', 'Budapest'), 16), (('green', 'Bucuresti'), ('green', 'Odessa'), 10),
          (('green', 'Moskwa'), ('orange', 'Sankt-Peterburg'), 14), (('green', 'Moskwa'), ('green', 'Minsk'), 14), (('green', 'Odessa'), ('green', 'Bucuresti'), 10),
          (('orange', 'Sankt-Peterburg'), ('green', 'Moskwa'), 14), (('yellow', 'Wien'), ('brown', 'Munchen'), 9), (('green', 'Minsk'), ('green', 'Kharkiv'), 16),
          (('brown', 'Munchen'), ('yellow', 'Wien'), 9), (('brown', 'Praha'), ('brown', 'Munchen'), 8)]

config['maps'] = {}
config['maps']['europe'] = europe

with open('config.json', 'w') as f:
  f.write(json.dumps(config, indent=2, sort_keys=True))