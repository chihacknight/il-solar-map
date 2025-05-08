const energized_colors = ['#fcfcfc', '#eff3ff', '#bdd7e7', '#6baed6', '#3182bd', '#08519c']
const planned_colors = ['#fcfcfc', '#f2f0f7', '#cbc9e2', '#9e9ac8', '#756bb1', '#54278f']

const geography_buckets = {
  'tracts': { 'total_kw': [0, 100, 1000, 5000, 10000, 50000],
              'utility_kw': [0, 900, 2000, 9900, 70000, 99000],
              'cs_kw': [0, 650, 900, 2000, 4000, 6000],
              'dg_large_kw': [0, 100, 300, 750, 1400, 2300],
              'dg_small_kw': [0, 100, 250, 500, 1000, 2000] },
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
  'il-house': { 'total_kw': [0, 20000, 40000, 80000, 150000, 300000],
                'utility_kw': [0, 10000, 50000, 100000, 200000, 300000],
                'cs_kw': [0, 2000, 6000, 10000, 15000, 20000],
                'dg_large_kw': [0, 1500, 5000, 10000, 15000, 20000],
                'dg_small_kw': [0, 100, 2000, 5000, 10000, 15000] },
  'il-senate': { 'total_kw': [0, 1000, 20000, 50000, 200000, 400000],
                  'utility_kw': [0, 25000, 50000, 100000, 200000, 400000],
                  'cs_kw': [0, 4000, 10000, 15000, 20000, 30000],
                  'dg_large_kw': [0, 2000, 5000, 10000, 15000, 20000],
                  'dg_small_kw': [0, 500, 2500, 10000, 15000, 20000] },
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

const geoButtonsSelector = '#geography-select button'
const catButtonsSelector = '#category-select button'
const statButtonsSelector = '#status-select button'
const hoverMsgDefault = 'Hover over a feature to see details'

class InfoControl {
  constructor() {
    this.container = document.createElement('div')
    this.container.className = 'info'
    this.container.innerHTML = hoverMsgDefault
  }

  onAdd(map) {
    this.map = map
    return this.container
  }

  onRemove() {
    this.container.parentNode.removeChild(this.container)
    this.map = undefined
  }

  updateInfo(content) {
    this.container.style.display = content ? 'block' : 'none'
    this.container.innerHTML = content
  }
}

function getTooltipHeader(props){
  let header = ''
  if (props.census_tract !== undefined) {
    header = `Tract ${props.census_tract}`
  } else if (props.place !== undefined) {
    header = `${props.place}`
  } else if (props.county_name !== undefined) {
    header = `${props.county_name} County`
  } else if (props.house_district !== undefined) {
    header = `IL House District ${props.house_district}
      <small><br />Rep. ${props.legislator} (${props.party})</small>`
  } else if (props.senate_district !== undefined) {
    header = `IL Senate District ${props.senate_district}
      <small><br />Sen. ${props.legislator} (${props.party})</small>`
  }
  return header
}

function getHoverTooltip(props){
  return `
    <strong>${getTooltipHeader(props)}</strong><br />
    ${friendly_category_names[selectedCategory]} Energized: ${props[selectedCategory].toLocaleString()} kW<br />
    ${friendly_category_names[selectedCategory]} Planned: ${props['planned_'+selectedCategory].toLocaleString()} kW
    `
}

function getTooltip(props){

  return `
    <h4>${getTooltipHeader(props)}</h4>
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
          <td><span class='float-end'>${props.utility_kw.toLocaleString()} kW</span></td>
          <td><span class='float-end'>${props.utility_count.toLocaleString()}</span></td>
          <td><span class='float-end'>${props.planned_utility_kw.toLocaleString()} kW</span></td>
          <td><span class='float-end'>${props.planned_utility_count.toLocaleString()}</span></td>
        </tr>
        <tr>
          <td>Community Solar</td>
          <td><span class='float-end'>${props.cs_kw.toLocaleString()} kW</span></td>
          <td><span class='float-end'>${props.cs_count.toLocaleString()}</span></td>
          <td><span class='float-end'>${props.planned_cs_kw.toLocaleString()} kW</span></td>
          <td><span class='float-end'>${props.planned_cs_count.toLocaleString()}</span></td>
        </tr>
        <tr>
          <td>Large DG</td>
          <td><span class='float-end'>${props.dg_large_kw.toLocaleString()} kW</span></td>
          <td><span class='float-end'>${props.dg_large_count.toLocaleString()}</span></td>
          <td><span class='float-end'>${props.planned_dg_large_kw.toLocaleString()} kW</span></td>
          <td><span class='float-end'>${props.planned_dg_large_count.toLocaleString()}</span></td>
        </tr>
        <tr>
          <td>Small DG</td>
          <td><span class='float-end'>${props.dg_small_kw.toLocaleString()} kW</span></td>
          <td><span class='float-end'>${props.dg_small_count.toLocaleString()}</span></td>
          <td><span class='float-end'>${props.planned_dg_small_kw.toLocaleString()} kW</span></td>
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

function resetClickedState(){
  // reset the previous clicked feature
  map.setFeatureState(
    { source: selectedGeography, id: selectedId },
    { clicked: false }
  )
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

function featureClicked(feature, lngLat=null){

  map.setFeatureState(
    { source: selectedGeography, id: feature.id },
    { clicked: true }
  )
  
  // collapse all coordinates to calculate bounds
  if (feature.geometry.type === 'Polygon' || feature.geometry.type === 'MultiPolygon') {
    const coordinates = feature.geometry.coordinates

    // Flatten all coordinates from all rings (and all polygons if MultiPolygon)
    let allCoords = []
    if (feature.geometry.type === 'Polygon') {
      allCoords = coordinates.flat()  // One polygon with rings
    } else {
      allCoords = coordinates.flat(2) // MultiPolygon
    }

    const bounds = allCoords.reduce((b, coord) => b.extend(coord), new maplibregl.LngLatBounds(allCoords[0], allCoords[0]))

    if (lngLat == null) {
      lngLat = bounds.getCenter()
    }

    // Fit to bounds
    map.fitBounds(bounds, {
      padding: 300,
      duration: 500,
      easing: t => t
    })
  }
  // Display info popup
  popup = new maplibregl.Popup()
    .setLngLat(lngLat)
    .setHTML(getTooltip(feature.properties))
    .addTo(map)
}

async function loadSourceFromGzip(url, map, layerSource) {
  const response = await fetch(url)
  const arrayBuffer = await response.arrayBuffer()
  const decompressedData = pako.inflate(new Uint8Array(arrayBuffer), { to: 'string' })
  const geojson = JSON.parse(decompressedData)

  map.addSource(layerSource, {
    type: 'geojson',
    data: geojson
  })

  addLayer(map, layerSource)

  if (selectedGeography == layerSource) {
    showLayer(selectedGeography, selectedCategory, selectedStatus)
    updateLegend(selectedGeography, selectedCategory, selectedStatus)
  }
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
      'fill-opacity': [
        'case',
        ['boolean', ['feature-state', 'hover'], false],
        0.7,
        0.5
      ]
    }
  })

  // polygon line styles
  map.addLayer({
    'id': `${layerSource}-outline`,
    'type': 'line',
    'source': layerSource, // reference the data source
    'layout': {
      // Make the layer not visible by default.
      'visibility': visible
    },
    'paint': {
      'line-color': [
        'case',
        ['boolean', ['feature-state', 'clicked'], false],
        '#000000',
        '#CCCCCC'
      ],
      'line-width': [
        'case',
        ['boolean', ['feature-state', 'clicked'], false],
        2,
        0.5
      ],
      'line-opacity': 1,
    }
  })
  
  map.on('mousemove', `${layerSource}-fills`, (e) => {
    // populate tooltip
    map.getCanvas().style.cursor = 'pointer'
    const feature = e.features[0]

    if (feature) {
      infoControl.updateInfo(getHoverTooltip(feature.properties))
      
      if (hoveredPolygonId !== null) {
        map.setFeatureState(
          { source: layerSource, id: hoveredPolygonId },
          { hover: false }
        )
      } else {
        infoControl.updateInfo(hoverMsgDefault)
      }

      // geojson data must have a unique id property (outside of properties)
      hoveredPolygonId = feature.id
      map.setFeatureState(
        { source: layerSource, id: hoveredPolygonId },
        { hover: true }
      )
    }
  })
  
  map.on('mouseleave', `${layerSource}-fills`, () => {
    map.getCanvas().style.cursor = ''
    map.setFeatureState(
      { source: layerSource, id: hoveredPolygonId },
      { hover: false }
    )
    infoControl.updateInfo(hoverMsgDefault)
  })

  map.on('click', `${layerSource}-fills`, (e) => {
    const feat = e.features[0]
    resetClickedState()
    selectedId = feat.id
    $.address.parameter('id', selectedId)
    featureClicked(feat, e.lngLat)
  })
}

function showLayer(selectedGeography, selectedCategory, selectedStatus) {  
  map.setLayoutProperty(selectedGeography + '-fills', 'visibility', 'visible')
  map.setLayoutProperty(selectedGeography + '-outline', 'visibility', 'visible')
  map.setPaintProperty(selectedGeography + '-fills', 'fill-color', getFillColor(selectedGeography, selectedCategory, selectedStatus))
  updateLegend(selectedGeography, selectedCategory, selectedStatus)

  // remove previous popup
  if (popup) {
    popup.remove()
    $.address.parameter('id', null)
  }
}

function hideLayers(layerIds) {
  layerIds.forEach(layerId => {
    map.setLayoutProperty(layerId, 'visibility', 'none')
  })
}

function toggleActive (selectorForSiblings, activeButton){
  $(selectorForSiblings).removeClass('active')
  $(selectorForSiblings).attr('aria-pressed', false)
  activeButton.classList.add('active')
  activeButton.setAttribute('aria-pressed', true)
}

function loadParam(param_name, param_default){
  let param = param_default
  let load_val = $.address.parameter(param_name)
  if (load_val != undefined) {
    param = load_val
  }
  
  if (param_default) {
    // sets the active and aria to the parameter
    toggleActive('#' + param_name + '-select button',$(':button[value=' + param + ']')[0])
  }
  return param
}

$(window).resize(function () {
  var h = $(window).height(),
    offsetTop = 125; // Calculate the top offset

  $('#map').css('height', (h - offsetTop));
}).resize();

const map = new maplibregl.Map({
    container: 'map', // container ID
    style: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json', // style URL
    center: [-89.189799, 40.166281], // starting position [lng, lat]
    zoom: 6, // starting zoom
})

const infoControl = new InfoControl()
map.addControl(infoControl, 'bottom-left')

let hoveredPolygonId = null

let selectedGeography = loadParam('geography','tracts')
let selectedCategory = loadParam('category','total_kw')
let selectedStatus = loadParam('status','energized')
let selectedId = loadParam('id', 0)
let selectedFeatureLoaded = false
let popup = null

map.on('load', () => {
  // load our 5 main data sources
  loadSourceFromGzip('/data/final/solar-projects-by-tract.geojson.gz', map, 'tracts')
  loadSourceFromGzip('/data/final/solar-projects-by-place.geojson.gz', map, 'places')
  loadSourceFromGzip('/data/final/solar-projects-by-county.geojson.gz', map, 'counties')
  loadSourceFromGzip('/data/final/solar-projects-by-il-senate.geojson.gz', map, 'il-senate')
  loadSourceFromGzip('/data/final/solar-projects-by-il-house.geojson.gz', map, 'il-house')

  $('#geography-select button').click(function(e){
    // reset layers
    hideLayers(['tracts-fills','places-fills','counties-fills','il-senate-fills','il-house-fills'])
    hideLayers(['tracts-outline','places-outline','counties-outline','il-senate-outline','il-house-outline'])
    
    resetClickedState()
    selectedGeography = this.value
    $.address.parameter('geography', selectedGeography)
    
    toggleActive(geoButtonsSelector, this)

    showLayer(selectedGeography, selectedCategory, selectedStatus)
  })

  $('#category-select button').click(function(e){
    
    selectedCategory = this.value
    $.address.parameter('category', selectedCategory)
    
    toggleActive(catButtonsSelector, this)

    showLayer(selectedGeography, selectedCategory, selectedStatus)
  })

  $('#status-select button').click(function(e){
    
    selectedStatus = this.value
    $.address.parameter('status', selectedStatus)
    
    toggleActive(statButtonsSelector, this)

    showLayer(selectedGeography, selectedCategory, selectedStatus)
  })

  // if an ID is in the URL, load it. 
  // waiting for sourcedata event to trigger before we can access features
  map.on('sourcedata', function (e) {
    if (
      !selectedFeatureLoaded &&
      selectedId &&
      e.sourceId === selectedGeography &&
      e.isSourceLoaded
    ) {
      selectedId = Number(selectedId)
      const features = map.querySourceFeatures(selectedGeography)
      const feat = features.find(f => f.id === selectedId)

      featureClicked(feat)

      // ensure this is only done once. sourcedata events are fired often
      selectedFeatureLoaded = true
    }
  })

})