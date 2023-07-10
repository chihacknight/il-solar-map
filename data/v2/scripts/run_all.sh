# /bin/bash

# combine 3 source files into one
python combine-projects.py

# look up centroids for each census tract we have
python get_tract_centroids.py

# aggregate data by county
python aggregate-data-by-county.py