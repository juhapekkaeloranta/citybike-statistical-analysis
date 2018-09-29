var MAP;

function addStationMarker(coordinates, markerTitle) {
  console.log('adding station markers')
  var marker = new google.maps.Marker({
    position: coordinates,
    map: MAP,
    title: markerTitle
  });
  marker.addListener('click', function () {
    console.log('clicked on:', marker.title)
  });
}

function initMap() {
  console.log('Initializing map')
  var styles = [
    {
      "featureType": "all",
      "elementType": "labels.text.fill",
      "stylers": [
        { "saturation": 36 },
        { "color": "#333333" },
        { "lightness": 40 }
      ]
    },
    {
      "featureType": "all",
      "elementType": "labels.text.stroke",
      "stylers": [
        { "visibility": "on" },
        { "color": "#ffffff" },
        { "lightness": 16 }]
    },
    {
      "featureType": "all",
      "elementType": "labels.icon",
      "stylers": [
        { "visibility": "off" }
      ]
    },
    {
      "featureType": "administrative",
      "elementType": "geometry.fill",
      "stylers": [
        { "color": "#fefefe" },
        { "lightness": 20 }
      ]
    },
    {
      "featureType": "administrative",
      "elementType": "geometry.stroke",
      "stylers": [
        { "color": "#fefefe" },
        { "lightness": 17 },
        { "weight": 1.2 }
      ]
    },
    {
      "featureType": "landscape",
      "elementType": "geometry",
      "stylers": [
        { "color": "#f5f5f5" },
        { "lightness": 20 }
      ]
    },
    {
      "featureType": "poi",
      "elementType": "geometry",
      "stylers": [
        { "color": "#f5f5f5" },
        { "lightness": 21 }]
    },
    {
      "featureType": "poi.park",
      "elementType": "geometry",
      "stylers": [
        { "color": "#e6e6e6" },
        { "lightness": 21 }
      ]
    },
    {
      "featureType": "road.highway",
      "elementType": "geometry.fill",
      "stylers": [
        { "color": "#ffffff" }, { "lightness": 17 }
      ]
    },
    {
      "featureType": "road.highway",
      "elementType": "geometry.stroke",
      "stylers": [
        { "color": "#ffffff" },
        { "lightness": 29 },
        { "weight": 0.2 }]
    },
    {
      "featureType": "road.arterial",
      "elementType": "geometry",
      "stylers": [
        { "color": "#ffffff" },
        { "lightness": 18 }]
    },
    {
      "featureType": "road.local",
      "elementType": "geometry",
      "stylers": [
        { "color": "#ffffff" },
        { "lightness": 16 }]
    },
    {
      "featureType": "transit",
      "elementType": "geometry",
      "stylers": [
        { "color": "#f2f2f2" },
        { "lightness": 19 }
      ]
    },
    {
      "featureType": "water",
      "elementType": "geometry",
      "stylers": [
        { "color": "#e0eff8" },
        { "lightness": 17 }
      ]
    }]

  var mapOptions = {
    zoom: 14,
    center: { lat: 60.175, lng: 24.939671 },
    disableDefaultUI: true,
    zoomControl: false,
    styles: styles
  }
  var mapDomElement = document.getElementById('map');

  MAP = new google.maps.Map(mapDomElement, mapOptions);

  //addStationMarkers()
}

function addStationMarkers() {
  var data = {
    "stations": [
      {
        "name": "Kaivopuisto",
        "total_slots": 30,
        "lat": "60.155411",
        "lon": "24.950391",
        "stationId": "001"
      },
      {
        "name": "Laivasillankatu",
        "total_slots": 12,
        "lat": "60.159715",
        "lon": "24.955212",
        "stationId": "002"
      },
      {
        "name": "Kapteeninpuistikko",
        "total_slots": 16,
        "lat": "60.158172",
        "lon": "24.944808",
        "stationId": "003"
      }
    ]
  }

  d3.json('stations.json', function (error, data) {
    data.stations.map(stat => {
      addStationMarker({ lat: parseFloat(stat.lat), lng: parseFloat(stat.lon)}, stat.stationId)
    })
  })
}