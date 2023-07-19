# il-solar-map

Data prep for ILSolarMap.com. 

Read more about ILSolarMap.com here: https://docs.google.com/document/d/1V4BLQhhcFK38FIupAo-gKgJXOfpIzCbdwdtMYjgMeBI/edit

![IlSolarMap.com](images/il-solar-map-x4.jpg)

## Setup
We recommend using [virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html) for working in a virtualized development environment. [Read how to set up virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Once you have virtualenvwrapper set up, do this:

```bash
mkvirtualenv il-solar-map -p /path/to/your/python3
pip install -r requirements.txt
```

## Running the Script

To run everything:

```bash
cd data/v2/scripts
bash run_all.sh
```

You can also run each script individually from the `data/v2/scripts` folder:

```bash
# combine 3 source files into one
python combine_projects.py

# assign il house and senate districts based on tract centroids
python get_tract_districts.py

# aggregate data by county, tract and legilsative districts
python aggregate_data.py
```

## Publishing data with kepler.gl

The interactive map is powered with [kepler.gl](https://kepler.gl/), an open source geospatial analysis tool.

The project is managed in kepler.gl and exported as an HTML page. This page is then renamed to `index.html` and [this patch is applied](https://github.com/keplergl/kepler.gl/pull/2292/files#r1268629776) to load the appropriate version of kepler.gl (2.5.5).

The site is then published with GitHub Pages.

## Data sources

Boundary sources

* Illinois Counties - https://clearinghouse.isgs.illinois.edu/data/reference/illinois-county-boundaries-polygons-and-lines
* Illinois State Senate Districts (2023) - https://www.elections.il.gov/shape/
* Illinois State House Districts (2023) - https://www.elections.il.gov/shape/
* Illinois Census Tracts - https://www2.census.gov/geo/tiger/TIGER2020PL/STATE/17_ILLINOIS/17/

Solar project sources

* Illinois Adjustable Block Program projects (Illinois Power Agency) - https://illinoisabp.com/project-application-reports/
* Illinois Solar for All program (Illinois Power Agency)
* Utility solar projects (US EIA-860M) - https://www.eia.gov/electricity/data/eia860m/

Legislator info

* Illinois State Senate Members - https://ballotpedia.org/Illinois_State_Senate
* Illinois State House Members - https://ballotpedia.org/Illinois_House_of_Representatives