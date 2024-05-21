const energized_colors = ['#fcfcfc', '#eff3ff', '#bdd7e7', '#6baed6', '#3182bd', '#08519c']
const planned_colors = ['#fcfcfc', '#f2f0f7', '#cbc9e2', '#9e9ac8', '#756bb1', '#54278f']

const geography_buckets = {
  'tracts': { 'total_kw': [0, 100, 1000, 5000, 10000, 50000],
              'utility_kw': [0, 900, 2000, 9900, 70000, 99000],
              'cs_kw': [0, 650, 900, 2000, 4000, 6000],
              'dg_large_kw': [0, 100, 300, 750, 1400, 2300],
              'dg_small_kw': [0, 70, 200, 350, 600, 1500] },
  'places': { 'total_kw': [0, 300, 1200, 3000, 6000, 10000],
              'utility_kw': [0, 300, 1100, 1500, 35000, 99000],
              'cs_kw': [0, 650, 900, 2000, 4000, 6000],
              'dg_large_kw': [0, 200, 700, 1350, 2200, 4000],
              'dg_small_kw': [0, 100, 400, 900, 2200, 4000] },
  'counties': { 'total_kw': [0, 7000, 23000, 43000, 70000, 150000],
                'utility_kw': [0, 2900, 9300, 20000, 70000, 149000],
                'cs_kw': [0, 2000, 4850, 8900, 14000, 17000],
                'dg_large_kw': [0, 800, 2200, 4200, 7600, 20000],
                'dg_small_kw': [0, 700, 2300, 6200, 12000, 21000] },
  'il-house': { 'total_kw': [0, 6500, 20000, 40000, 80000, 150000],
                'utility_kw': [0, 2000, 8000, 17000, 72000, 151000],
                'cs_kw': [0, 900, 2000, 4000, 8000, 15000],
                'dg_large_kw': [0, 900, 2400, 3900, 6100, 8500],
                'dg_small_kw': [0, 800, 1600, 2500, 3900, 6700] },
  'il-senate': { 'total_kw': [0, 9000, 20000, 40000, 70000, 130000],
                  'utility_kw': [0, 4000, 12000, 25000, 74000, 206000],
                  'cs_kw': [0, 900, 3900, 8600, 12000, 25000],
                  'dg_large_kw': [0, 1300, 2700, 4100, 7000, 12000],
                  'dg_small_kw': [0, 1700, 3900, 5600, 7600, 11000] },
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
          <th><span class='float-end'>Energized</span></th>
          <th><span class='float-end'>#</span></th>
          <th><span class='float-end'>Planned</span></th>
          <th><span class='float-end'>#</span></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Total</td>
          <td><span class='float-end'>${props.total_kw.toLocaleString()} kW</span></td>
          <td><span class='float-end'>${props.total_count.toLocaleString()}</span></td>
          <td><span class='float-end'>${props.planned_total_kw.toLocaleString()} kW</span></td>
          <td><span class='float-end'>${props.planned_total_count.toLocaleString()}</span></td>
        </tr>
        <tr>
          <td>Utility</td>
          <td><span class='float-end'>${props.utility_kw.toLocaleString()}kW</span></td>
          <td><span class='float-end'>${props.utility_count.toLocaleString()}</span></td>
          <td><span class='float-end'>${props.planned_utility_kw.toLocaleString()}kW</span></td>
          <td><span class='float-end'>${props.planned_utility_count.toLocaleString()}</span></td>
        </tr>
        <tr>
          <td>Community Solar</td>
          <td><span class='float-end'>${props.cs_kw.toLocaleString()}kW</span></td>
          <td><span class='float-end'>${props.cs_count.toLocaleString()}</span></td>
          <td><span class='float-end'>${props.planned_cs_kw.toLocaleString()}kW</span></td>
          <td><span class='float-end'>${props.planned_cs_count.toLocaleString()}</span></td>
        </tr>
        <tr>
          <td>Large DG</td>
          <td><span class='float-end'>${props.dg_large_kw.toLocaleString()}kW</span></td>
          <td><span class='float-end'>${props.dg_large_count.toLocaleString()}</span></td>
          <td><span class='float-end'>${props.planned_dg_large_kw.toLocaleString()}kW</span></td>
          <td><span class='float-end'>${props.planned_dg_large_count.toLocaleString()}</span></td>
        </tr>
        <tr>
          <td>Small DG</td>
          <td><span class='float-end'>${props.dg_small_kw.toLocaleString()}kW</span></td>
          <td><span class='float-end'>${props.dg_small_count.toLocaleString()}</span></td>
          <td><span class='float-end'>${props.planned_dg_small_kw.toLocaleString()}kW</span></td>
          <td><span class='float-end'>${props.planned_dg_small_count.toLocaleString()}</span></td>
        </tr>
      </tbody>
    </table>
  `
}

function updateLegend(layerSource, category, status){
  let legendText = `<strong>${friendly_category_names[category]} kW of solar ${status}<br />by ${friendly_geography_names[layerSource]}</strong>`
  let buckets = geography_buckets[layerSource][category]

  let colors = energized_colors
  if (status == 'planned') {
    colors = planned_colors
  }

  for (var i = 0; i < buckets.length; i++) {
    if (i == buckets.length - 1) {
      legendText += `<div><span style="background-color: ${colors[i]}"></span>${buckets[i].toLocaleString()}+ kW</div>`
    } else {
      legendText += `<div><span style="background-color: ${colors[i]}"></span>${buckets[i].toLocaleString()} - ${(buckets[i+1] - 1).toLocaleString()} kW</div>`
    }
  }

  $('#solar-legend').html(legendText)
}

function getFillColor(layerSource, category, status){
  let var_prefix = ""
  let colors = energized_colors
  if (status == 'planned') {
    var_prefix = "planned_"
    colors = planned_colors
  }

  let buckets = geography_buckets[layerSource][category]
  let fillColor = ['interpolate', ['linear'], ['get', var_prefix + category]]
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
      'fill-color': getFillColor(layerSource, 'total_kw', "energized"),
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

function showLayer(selectedGeography, selectedCategory, selectedStatus) {
  map.setLayoutProperty(selectedGeography + '-fills', 'visibility', 'visible')
  map.setPaintProperty(selectedGeography + '-fills', 'fill-color', getFillColor(selectedGeography, selectedCategory, selectedStatus))
  updateLegend(selectedGeography, selectedCategory, selectedStatus)
}

function loadParam(param_name, param_default){
  let param = param_default
  let load_val = $.address.parameter(param_name)
  if (load_val != undefined) {
    param = load_val
  }
  // set buttons
  $('#' + param_name + '-select button').removeClass('active')
  $(':button[value=' + param + ']')[0].classList.add('active')
  
  return param
}

$(window).resize(function () {
  var h = $(window).height(),
    offsetTop = 125; // Calculate the top offset

  $('#map').css('height', (h - offsetTop));
}).resize();

mapboxgl.accessToken = 'pk.eyJ1IjoiZGF0YW1hZGUiLCJhIjoiaXhhVGNrayJ9.0yaccougI3vSAnrKaB00vA'
const map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/light-v11', // style URL
    center: [-89.189799, 40.166281], // starting position [lng, lat]
    zoom: 6, // starting zoom
})

let hoveredPolygonId = null

let selectedGeography = loadParam('geography','tracts')
let selectedCategory = loadParam('category','total_kw')
let selectedStatus = loadParam('status','energized')

map.on('load', () => {
  // load our 4 main data sources
  map.addSource('tracts', {
      type: 'geojson',
      data: '/data/final/solar-projects-by-tract.geojson'
  })

  map.addSource('places', {
    type: 'geojson',
    data: '/data/final/solar-projects-by-place.geojson'
  })

  map.addSource('counties', {
      type: 'geojson',
      data: '/data/final/solar-projects-by-county.geojson'
  })

  map.addSource('il-house', {
      type: 'geojson',
      data: '/data/final/solar-projects-by-il-house.geojson'
  })

  map.addSource('il-senate', {
      type: 'geojson',
      data: '/data/final/solar-projects-by-il-senate.geojson'
  })

  addLayer(map, 'tracts')
  addLayer(map, 'places')
  addLayer(map, 'counties')
  addLayer(map, 'il-senate')
  addLayer(map, 'il-house')
  showLayer(selectedGeography, selectedCategory, selectedStatus)
  updateLegend(selectedGeography, selectedCategory, selectedStatus)

  $('#geography-select button').click(function(e){
    // reset layers
    map.setLayoutProperty('tracts-fills', 'visibility', 'none')
    map.setLayoutProperty('places-fills', 'visibility', 'none')
    map.setLayoutProperty('counties-fills', 'visibility', 'none')
    map.setLayoutProperty('il-senate-fills', 'visibility', 'none')
    map.setLayoutProperty('il-house-fills', 'visibility', 'none')
    $('#geography-select button').removeClass('active')
    
    selectedGeography = this.value
    $.address.parameter('geography', selectedGeography)
    this.classList.add('active')
    showLayer(selectedGeography, selectedCategory, selectedStatus)
  })

  $('#category-select button').click(function(e){
    $('#category-select button').removeClass('active')
    
    selectedCategory = this.value
    $.address.parameter('category', selectedCategory)
    this.classList.add('active')
    showLayer(selectedGeography, selectedCategory, selectedStatus)
  })

  $('#status-select button').click(function(e){
    $('#status-select button').removeClass('active')
    
    selectedStatus = this.value
    $.address.parameter('status', selectedStatus)
    this.classList.add('active')
    showLayer(selectedGeography, selectedCategory, selectedStatus)
  })
})