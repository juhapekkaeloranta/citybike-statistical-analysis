if (APIKEY) {
  console.log('apikey found!')

  function addScriptElementToDocument(url) {
    var script = document.createElement("script");
    script.src = url
    document.body.appendChild(script);
  }
  
  addScriptElementToDocument("https://maps.googleapis.com/maps/api/js?key=" + APIKEY + "&callback=initMap")
} else {
  console.log('apikey not found')
}