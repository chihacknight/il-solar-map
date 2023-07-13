# /bin/bash

# look up centroids for each census tract we have
python get_tract_centroids.py

# combine 3 source files into one
python combine_projects.py

# aggregate data by county, tract and legilsative district
python aggregate_data.py