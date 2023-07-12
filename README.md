# il-solar-map

Data prep for ILSolarMap.com. 

Read more about ILSolarMap.com here: https://docs.google.com/document/d/1V4BLQhhcFK38FIupAo-gKgJXOfpIzCbdwdtMYjgMeBI/edit

![IlSolarMap.com](images/ilsolarmap.jpg)

## Setup
Install the base package requirements: ```pip install -r requirements.txt```

## Running the Script
First cd into the v2 folder with ```cd data/v2/ ```
Then run ```python3 combine-projects.py``` to update and generate a file containing all the projects
To see aggregates by county, run ```python3 aggregate-by-county.py```

## Data sources

Boundary sources

* Illinois Counties - https://clearinghouse.isgs.illinois.edu/data/reference/illinois-county-boundaries-polygons-and-lines
* Illinois State Senate Districts (2023) - https://www.elections.il.gov/shape/
* Illinois State House Districts (2023) - https://www.elections.il.gov/shape/
* Illinois Census Tracts - https://www2.census.gov/geo/tiger/TIGER2020PL/STATE/17_ILLINOIS/17/

Solar project sources

* Illinois Adjustable Block Program projects (Illinois Power Agency)
* Illinois Solar for All program (Illinois Power Agency)
* Utility solar projects (US EIA Energy Atlas)
