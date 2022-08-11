const tunjaPosition = ol.proj.fromLonLat([-73.366379, 5.538590]);

function loadMap() {
  var map = new ol.Map({
    target: 'map',
    layers: [ new ol.layer.Tile({ source: new ol.source.OSM() }) ],
    view: new ol.View({
      center: tunjaPosition,
      zoom: 9,
      minZoom: 4
    })
  });

  map.on('click', function(evt) {
    const select = ol.proj.transform(evt.coordinate, 'EPSG:3857', 'EPSG:4326');
    $('#longitude-form').val(select[0])
    $('#latitude-form').val(select[1])
  });
}

$('#map-modal').on('shown.bs.modal', function () {
  loadMap();
})

const showInfo = (value) => {
  if(value) {
    window.location.replace('/bus')
  } else {
    alert('El estudiante no se encuentra en el bus!')
  }
}

$(document).ready(()=> {
  var socket = io();

  socket.on('connect', ()=> {
    
  });

  socket.on('code', (data) => {
    $('#code').text(data)
    $('#code-form').val(data)
  });
 
})