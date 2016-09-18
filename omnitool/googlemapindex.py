index = """"<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>"""

index2 = """</title>
    <style>
      html, body { height: 100%; margin: 0; padding: 0; }
      #map { height: 100%; }
      #coords { background-color: black; color: white; padding: 5px; }
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script>


function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 1,
    center: {lat: 30, lng: 50},
    mapTypeControl: false,
	backgroundColor: '#84AAF8'
  });

  initTerraria();
  map.mapTypes.set('Terraria', TerrariaMapType);
  map.setMapTypeId('Terraria');
}

var TerrariaMapType;
function initTerraria() {

  TerrariaMapType = new google.maps.ImageMapType({
    getTileUrl: function(coord, zoom) {

      return 'tiles/screen_' + (zoom-2) + '_' + coord.x + '_' + coord.y + '.png';
    },
    tileSize: new google.maps.Size(1600, 1600),
    isPng: true,
    minZoom: 3,
    maxZoom: 6,
    name: 'Terraria'
  });



}

    </script>
    <script async defer
        src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDobT-f8VWyp2RdjKRijTsLlFpPpMjj0dQ&callback=initMap"></script>
  </body>
</html>"""