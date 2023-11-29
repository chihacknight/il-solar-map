# il-solar-map

Website and data prep for ILSolarMap.com. 

![IlSolarMap.com](images/il-solar-map-x4.jpg)

## Setup
We recommend using [virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html) for working in a virtualized development environment. [Read how to set up virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Once you have virtualenvwrapper set up, do this:

```bash
mkvirtualenv il-solar-map -p /path/to/your/python3
pip install -r requirements.txt
```

## Running the data aggregation scripts

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

We replace part of the html header meta tags for the site for custom title, description and image:

```html
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8"/>
        <title>Illinois Solar Map - Chi Hack Night / ICJC</title>

        <!--Uber Font-->
        <link rel="stylesheet" href="https://d1a3f4spazzrp4.cloudfront.net/kepler.gl/uber-fonts/4.0.0/superfine.css">

        <!--MapBox css-->
        <link href="https://api.tiles.mapbox.com/mapbox-gl-js/v1.1.1/mapbox-gl.css" rel="stylesheet">

        <!-— facebook open graph tags -->
        <meta property="og:url" content="http://ilsolarmap.com/" />
        <meta property="og:title" content="Illinois Solar Map - Chi Hack Night / ICJC" />
        <meta property="og:description" content="See how and where over 1,800,000 kilowatts of solar have been installed by zip code in the State of Illinois" />
        <meta property="og:site_name" content="Illinois Solar Map" />
        <meta property="og:image" content="https://ilsolarmap.com/images/il-solar-map-x4.jpg" />
        <meta property="og:image:type" content="image/png" />
        <meta property="og:image:width" content="800" />
        <meta property="og:image:height" content="800" />

        <!-— twitter card tags -->
        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:site" content="Illinois Solar Map">
        <meta name="twitter:creator" content="Chi Hack Night / ICJC">
        <meta name="twitter:title" content="Illinois Solar Map - Chi Hack Night / ICJC">
        <meta name="twitter:description" content="See how and where over 1,800,000 kilowatts of solar have been installed in the State of Illinois">
        <meta name="twitter:image" content="https://ilsolarmap.com/images/il-solar-map-x4.jpg" />

        <!-- Load React/Redux -->
        <script src="https://unpkg.com/react@16.8.4/umd/react.production.min.js" crossorigin></script>
        <script src="https://unpkg.com/react-dom@16.8.4/umd/react-dom.production.min.js" crossorigin></script>
        <script src="https://unpkg.com/redux@3.7.2/dist/redux.js" crossorigin></script>
        <script src="https://unpkg.com/react-redux@7.1.3/dist/react-redux.min.js" crossorigin></script>
        <script src="https://unpkg.com/styled-components@4.1.3/dist/styled-components.min.js" crossorigin></script>

        <!-- Load Kepler.gl -->
        <script src="https://unpkg.com/kepler.gl@2.5.5/umd/keplergl.min.js" crossorigin></script>

        <style type="text/css">
          body {margin: 0; padding: 0; overflow: hidden;}
        </style>

        <!--MapBox token-->
        <script>
          /**
           * Provide your MapBox Token
           **/
          const MAPBOX_TOKEN = 'pk.eyJ1IjoiZGF0YW1hZGUiLCJhIjoiaXhhVGNrayJ9.0yaccougI3vSAnrKaB00vA';
          const WARNING_MESSAGE = 'Please Provide a Mapbox Token in order to use Kepler.gl. Edit this file and fill out MAPBOX_TOKEN with your access key';
        </script>

            
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-F7WESE4Z2K"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', 'G-F7WESE4Z2K');
        </script>

      </head>
```

## Setting up and running the website 

This site uses Jekyll to serve several static pages and images. The site is published to GitHub Pages.
### Dependencies

* [Jekyll](http://jekyllrb.com/) - Static site generator built in Ruby
* [Bootstrap 5](http://getbootstrap.com) - HTML and CSS layouts
* [DataTables](http://datatables.net) - for searching and sorting tables
* [CSV to HTML Table](https://github.com/derekeder/csv-to-html-table) - for sortable rollup tables

### Running locally

Requirements:

* ruby-2.6.2
* jekyll 3.1.6

We recommend using [rvm](https://rvm.io/) to manage your Ruby versions.

Initial setup
```console
git clone https://github.com/chihacknight/il-solar-map.git
cd il-solar-map
rvm install ruby-2.6.2
bundle install jekyll -v 3.1.6
bundle install
```

Running locally
```console
jekyll serve -w
```

Then open your web browser and navigate to http://localhost:3000

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