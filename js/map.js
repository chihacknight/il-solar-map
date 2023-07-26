function getTooltip(props){
  return `
    <h4>Tract ${props.census_tract}</h4>
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


mapboxgl.accessToken = 'pk.eyJ1IjoiZGF0YW1hZGUiLCJhIjoiaXhhVGNrayJ9.0yaccougI3vSAnrKaB00vA';
const map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/light-v11', // style URL
    center: [-89.189799, 40.166281], // starting position [lng, lat]
    zoom: 6, // starting zoom
});

let hoveredPolygonId = null;

map.on('load', () => {
  // load our 4 main data sources
  map.addSource('tracts', {
      type: 'geojson',
      data: '/data/v2/final/solar-projects-by-tract.geojson'
  });

  map.addSource('counties', {
      type: 'geojson',
      data: '/data/v2/final/solar-projects-by-county.geojson'
  });

  map.addSource('il-house', {
      type: 'geojson',
      data: '/data/v2/final/solar-projects-by-il-house.geojson'
  });

  map.addSource('il-senate', {
      type: 'geojson',
      data: '/data/v2/final/solar-projects-by-il-senate.geojson'
  });

  map.addLayer({
    'id': 'tract-fills',
    'type': 'fill',
    'source': 'tracts', // reference the data source
    'layout': {},
    'paint': {
      'fill-color': [
        'interpolate',
        ['linear'],
        ['get', 'total_kw'],
        0, '#FFFFFF',
        100, '#ECF0F6',
        250, '#B2C2DB',
        300, '#9BB0D0',
        500, '#849EC5',
        1000, '#6182B5',
        2000, '#4E71A6',
        210000, '#43618F',
      ],
      'fill-opacity': 0.5,
      'fill-outline-color': [
        'case',
        ['boolean', ['feature-state', 'hover'], false],
        '#000000',
        '#CCCCCC'
      ]
    }
  });

  const popup = new mapboxgl.Popup({
    closeButton: false,
    closeOnClick: false
  });
  
  map.on('mousemove', 'tract-fills', (e) => {
    // populate tooltip
    map.getCanvas().style.cursor = 'pointer';
    const coordinates = e.lngLat;
    popup.setLngLat(coordinates).setHTML(getTooltip(e.features[0].properties)).addTo(map);

    // highlight tract
    if (e.features.length > 0) {
      if (hoveredPolygonId !== null) {
        map.setFeatureState(
          { source: 'tracts', id: hoveredPolygonId },
          { hover: false }
        );
      }

      // geojson data must have a unique id property (outside of properties)
      hoveredPolygonId = e.features[0].id;
      map.setFeatureState(
        { source: 'tracts', id: hoveredPolygonId },
        { hover: true }
      );
    }
  });
  
  map.on('mouseleave', 'tract-fills', () => {
    map.getCanvas().style.cursor = '';
    popup.remove();
  });

});