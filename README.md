# nj-house-search

Collection of scripts and notebooks to assist in searching for a house in NJ. Main contributions are:
- allowing to sort/filter on GSMLS by additional attributes such as taxes and interior square footage
- add commute times to a destination (i.e work, Port Authority NYC) via google maps directions api for each address and allowsing sorting/filtering by this

Entrypoint is [analysis.ipynb](https://github.com/AlJohri/nj-house-search/blob/master/analysis.ipynb).

#### Setup

```
pipenv install
pipenv run jupyter nbextension enable --py widgetsnbextension --sys-prefix
```

#### Usage

``` 
pipenv run make
```

#### Future Work?

- handle addresses that google maps can't handle properly by first adding drive time to nearest park and ride and then transit time from there. google maps can't handle drive + transit very well
- replace or incorporate [nj transit trip planner](http://www.njtransit.com/sf/sf_servlet.srv?hdnPageAction=TripPlannerTo) since it handles finding the nearest station / park and ride and will do both train and bus. it also handles the farther places a bit better than google does
- cross reference Zillow for square footage. many GSMLS listings don't have the square footage
- incorporate NJMLS listings
