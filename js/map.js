const colors = ['#fcfcfc', '#eff3ff', '#bdd7e7', '#6baed6', '#3182bd', '#08519c']

const geography_buckets = {
  'tracts': [0, 100, 250, 500, 1000, 2000],
  'places': [0, 300, 1200, 3000, 6000, 10000],
  'counties': [0, 7000, 23000, 43000, 70000, 150000],
  'il-house': [0, 6000, 20000, 40000, 80000, 150000],
  'il-senate': [0, 9000, 20000, 40000, 70000, 130000]
}

const friendly_geography_names = {
  'tracts': 'Census Tract',
  'places': 'Place',
  'counties': 'County',
  'il-house': 'IL House District',
  'il-senate': 'IL Senate District'
}

const friendly_category_names = {
  'total_kw': 'All',
  'utility_kw': 'Utility',
  'cs_kw': 'Community Solar',
  'dg_large_kw': 'Large DG',
  'dg_small_kw': 'Small DG'
}

let selectedLayer = 'tracts'
let selectedCategory = 'total_kw'

function getTooltip(props){
  let header = ''
  if (props.census_tract !== undefined) {
    header = `<strong>Tract ${props.census_tract}</strong><br />`
  } else if (props.place !== undefined) {
    header = `<strong>${props.place}</strong><br />`
  } else if (props.county_name !== undefined) {
    header = `<strong>${props.county_name} County</strong><br />`
  } else if (props.house_district !== undefined) {
    header = `
    <strong>IL House District ${props.house_district}</strong><br />
      <strong>Rep. ${props.legislator} (${props.party})</strong><br />
      `
  } else if (props.senate_district !== undefined) {
    header = `
      <strong>IL Senate District ${props.senate_district}</strong><br />
      <strong>Sen. ${props.legislator} (${props.party})</strong><br />
      `
  }

  return `
    ${header}
    <table class='table table-sm map-tooltip'>
      <thead>
        <tr>
          <th>Category</th>
          <th><span class='float-end'>kW</span></th>
          <th><span class='float-end'>Projects</span></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Total</td>
          <td><span class='float-end'>${props.total_kw.toLocaleString()}kW</span></td>
          <td><span class='float-end'>${props.total_count.toLocaleString()}</span></td>
        </tr>
        <tr>
          <td>Utility</td>
          <td><span class='float-end'>${props.utility_kw.toLocaleString()}kW</span></td>
          <td><span class='float-end'>${props.utility_count.toLocaleString()}</span></td>
        </tr>
        <tr>
          <td>Community Solar</td>
          <td><span class='float-end'>${props.cs_kw.toLocaleString()}kW</span></td>
          <td><span class='float-end'>${props.cs_count.toLocaleString()}</span></td>
        </tr>
        <tr>
          <td>Large DG</td>
          <td><span class='float-end'>${props.dg_large_kw.toLocaleString()}kW</span></td>
          <td><span class='float-end'>${props.dg_large_count.toLocaleString()}</span></td>
        </tr>
        <tr>
          <td>Small DG</td>
          <td><span class='float-end'>${props.dg_small_kw.toLocaleString()}kW</span></td>
          <td><span class='float-end'>${props.dg_small_count.toLocaleString()}</span></td>
        </tr>
      </tbody>
    </table>
  `
}

function updateLegend(layerSource, category){
  let legendText = `<strong>${friendly_category_names[category]} kW of solar installed<br />by ${friendly_geography_names[layerSource]}</strong>`
  let buckets = geography_buckets[layerSource]

  for (var i = 0; i < buckets.length; i++) {
    if (i == buckets.length - 1) {
      legendText += `<div><span style="background-color: ${colors[i]}"></span>${buckets[i].toLocaleString()}+ kW</div>`
    } else {
      legendText += `<div><span style="background-color: ${colors[i]}"></span>${buckets[i].toLocaleString()} - ${(buckets[i+1] - 1).toLocaleString()} kW</div>`
    }
  }

  $('#solar-legend').html(legendText)
}

function getFillColor(layerSource, category){
  let buckets = geography_buckets[layerSource]
  let fillColor = ['interpolate', ['linear'], ['get', category]]
  for (var i = 0; i < buckets.length; i++) {
    fillColor.push(buckets[i], colors[i])
  }
  return fillColor
}

function addLayer(map, layerSource, visible = 'none'){
  map.addLayer({
    'id': `${layerSource}-fills`,
    'type': 'fill',
    'source': layerSource, // reference the data source
    'layout': {
      // Make the layer not visible by default.
      'visibility': visible
      },
    'paint': {
      'fill-color': getFillColor(layerSource, 'total_kw'),
      'fill-opacity': 0.5,
      'fill-outline-color': [
        'case',
        ['boolean', ['feature-state', 'hover'], false],
        '#000000',
        '#CCCCCC'
      ]
    }
  })

  const popup = new mapboxgl.Popup({
    closeButton: false,
    closeOnClick: false
  })
  
  map.on('mousemove', `${layerSource}-fills`, (e) => {
    // populate tooltip
    map.getCanvas().style.cursor = 'pointer'
    const coordinates = e.lngLat
    popup.setLngLat(coordinates).setHTML(getTooltip(e.features[0].properties)).addTo(map)

    // highlight tract
    if (e.features.length > 0) {
      if (hoveredPolygonId !== null) {
        map.setFeatureState(
          { source: layerSource, id: hoveredPolygonId },
          { hover: false }
        )
      }

      // geojson data must have a unique id property (outside of properties)
      hoveredPolygonId = e.features[0].id
      map.setFeatureState(
        { source: layerSource, id: hoveredPolygonId },
        { hover: true }
      )
    }
  })
  
  map.on('mouseleave', `${layerSource}-fills`, () => {
    map.getCanvas().style.cursor = ''
    popup.remove()
  })
}


mapboxgl.accessToken = 'pk.eyJ1IjoiZGF0YW1hZGUiLCJhIjoiaXhhVGNrayJ9.0yaccougI3vSAnrKaB00vA'
const map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/light-v11', // style URL
    center: [-89.189799, 40.166281], // starting position [lng, lat]
    zoom: 6, // starting zoom
})

let hoveredPolygonId = null

map.on('load', () => {
  // load our 4 main data sources
  map.addSource('tracts', {
      type: 'geojson',
      data: '/data/v2/final/solar-projects-by-tract.geojson'
  })

  map.addSource('places', {
    type: 'geojson',
    data: '/data/v2/final/solar-projects-by-place.geojson'
  })

  map.addSource('counties', {
      type: 'geojson',
      data: '/data/v2/final/solar-projects-by-county.geojson'
  })

  map.addSource('il-house', {
      type: 'geojson',
      data: '/data/v2/final/solar-projects-by-il-house.geojson'
  })

  map.addSource('il-senate', {
      type: 'geojson',
      data: '/data/v2/final/solar-projects-by-il-senate.geojson'
  })

  addLayer(map, 'tracts', 'visible')
  addLayer(map, 'places')
  addLayer(map, 'counties')
  addLayer(map, 'il-senate')
  addLayer(map, 'il-house')
  updateLegend('tracts', 'total_kw')

  $('#geography-select button').click(function(e){
    // reset layers
    map.setLayoutProperty('tracts-fills', 'visibility', 'none')
    map.setLayoutProperty('places-fills', 'visibility', 'none')
    map.setLayoutProperty('counties-fills', 'visibility', 'none')
    map.setLayoutProperty('il-senate-fills', 'visibility', 'none')
    map.setLayoutProperty('il-house-fills', 'visibility', 'none')
    $('#geography-select button').removeClass('active')
    
    selectedLayer = this.value
    this.classList.add('active')
    map.setLayoutProperty(selectedLayer + '-fills', 'visibility', 'visible')
    map.setPaintProperty(selectedLayer + '-fills', 'fill-color', getFillColor(selectedLayer, selectedCategory))
    updateLegend(selectedLayer, selectedCategory)
  })

  $('#category-select button').click(function(e){
    $('#category-select button').removeClass('active')
    
    selectedCategory = this.value
    this.classList.add('active')
    map.setPaintProperty(selectedLayer + '-fills', 'fill-color', getFillColor(selectedLayer, selectedCategory))
    updateLegend(selectedLayer, selectedCategory)
  })
})