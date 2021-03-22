# Leaf

## Usage

```py
from cannlytics.traceability import leaf

trace = leaf.authorize(api_key='xyz', mme_code='abc')
lab_result = trace.create_lab_result(data)
print(lab_result.summary())
```

## Inspiration

- [Gspread](https://github.com/burnash/gspread/blob/master/gspread/models.py)
- [Spotipy](https://github.com/plamere/spotipy/blob/master/spotipy/client.py)
- [Pythentic Jobs](https://github.com/ryanmcgrath/pythentic_jobs/blob/master/pythentic_jobs.py)
