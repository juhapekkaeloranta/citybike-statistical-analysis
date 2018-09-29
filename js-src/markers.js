function addStationMarker(coordinates, markerTitle) {
  console.log('adding station markers')
  var defaultIcon = {
    path: google.maps.SymbolPath.CIRCLE,
    scale: 5,
    strokeColor: '#000000',
    strokeOpacity: 0.8,
    strokeWeight: 0,
    fillColor: '#000000',
    fillOpacity: 0.7,
  }
  var marker = new google.maps.Marker({
    position: coordinates,
    map: MAP,
    title: markerTitle,
    icon: defaultIcon
  })
  marker.addListener('click', function () {
    console.log('clicked on:', marker.title)
  });
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