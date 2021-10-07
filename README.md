# banditrecommender
A multi-armed bandit recommender POC.


## Install the requirements

```
virutalenv env -p python3.8
source env/bin/activate
pip install -r requirements.txt 
```

## Launch the recommender

```
python app.py
```

This will create a test sequence of recommendations:

```buildoutcfg
(env) ➜  banditrecommender git:(main) ✗ python app.py
['skirts', 'jumpers', 'cardigans', 'bags', 'necklaces']
['jumpers', 'skirts', 'bags', 'cardigans', 'necklaces']
['cardigans', 'skirts', 't-shirts', 'bags', 'jumpers']
['skirts', 'bags', 'necklaces', 'cardigans', 'jumpers']
['t-shirts', 'skirts', 'necklaces', 'cardigans', 'jumpers']
...
['skirts', 'jumpers', 'necklaces', 't-shirts', 'cardigans']
['skirts', 'necklaces', 'bags', 'cardigans', 'jumpers']
['skirts', 'necklaces', 't-shirts', 'bags', 'jumpers']
['skirts', 'cardigans', 'necklaces', 't-shirts', 'bags']
['skirts', 'necklaces', 'bags', 'jumpers', 't-shirts']
['skirts', 'cardigans', 'bags', 'necklaces', 't-shirts']
```
