MARKERS = []

function addStationMarker(coordinates, stationId) {
  console.log('adding station markers')
  var defaultIcon = {
    path: google.maps.SymbolPath.CIRCLE,
    scale: 10,
    strokeColor: '#000000',
    strokeOpacity: 0.8,
    strokeWeight: 0,
    fillColor: '#000000',
    fillOpacity: 0.7,
  }
  var marker = new google.maps.Marker({
    position: coordinates,
    map: MAP,
    title: stationId,
    icon: defaultIcon
  })
  marker.addListener('click', function () {
    drawPopup(marker)
  });
  MARKERS.push({markerId: stationId, marker: marker})
}

function editMarkerSize(markerId, scale) {
  marker = MARKERS[0].marker
  marker.setMap(null)
  var editedMarker = new google.maps.Marker({
    position: marker.position,
    map: MAP,
    title: marker.title,
    icon: { ...marker.icon, scale: scale}
  })
  MARKERS.push({markerId: marker.stationId, marker: editedMarker})
}

function editMarkerColor(markerId, color) {
  marker = MARKERS[0].marker
  marker.setMap(null)
  var editedMarker = new google.maps.Marker({
    position: marker.position,
    map: MAP,
    title: marker.title,
    icon: { ...marker.icon, fillColor: color}
  })
  MARKERS.push({markerId: marker.stationId, marker: editedMarker})
}

function addStationMarkers() {
  d3.json("/data/station-locations.json", function (error, data) {
    console.log(error)
    console.log(data)
    data.stations.map(stat => {
      addStationMarker({ lat: parseFloat(stat.lat), lng: parseFloat(stat.lon)}, stat.stationId)
    })
  })
}

function removeMarkers() {
  MARKERS.map(markerObj => {
   marker.setMap(null);
  });
  MARKERS = []
}