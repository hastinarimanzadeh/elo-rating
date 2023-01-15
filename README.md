# Reference implementation of Elo rating system 

## Installation
```bash
$ python -m pip install -U elo_rating
```
## Example Usage
```python
from elo_rating import Elo

e = Elo()
e.add_match("p1", "p2", 1.0, k=0.15)
e.add_matches([("p1", "p2", 1.0), ("p2", "p1", 0.5)], k=0.15)

e.ratings() # {"p1": 0.13363123747494593, "p2": -0.1336312374749459}
e.items() # ['p1', 'p2']
e.rankings() # {'p1': 0, 'p2': 1}

e.ranking('p1') # 0
e.rating('p1')  # 0.13363123747494593 
```
