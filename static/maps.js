const tunjaPosition = ol.proj.fromLonLat([-73.366379, 5.538590]);

var map = new ol.Map({
  target: 'map',
  layers: [ new ol.layer.Tile({ source: new ol.source.OSM() }) ],
  view: new ol.View({
    center: tunjaPosition,
    zoom: 9,
    minZoom: 4
  })
});

let circleStyle = new ol.style.Circle({
  fill: new ol.style.Fill({ color: [249, 49, 5, 1] }),
  radius: 7,
})

const layer = new ol.layer.Vector({
  source: new ol.source.Vector({
    features: [
      new ol.Feature({
        geometry: new ol.geom.Point(tunjaPosition)
      })
    ]
  }),
  style: new ol.style.Style({ image: circleStyle })
});
map.addLayer(layer);

$(document).ready(()=> {
  var socket = io();

  socket.on('connect', ()=> {
    
  });
  
  socket.on('position', (data) => {
    let lat = data.lat;
    let lng = data.lng;
    layer.getSource().clear();
    layer.setSource(new ol.source.Vector({
      features: [
        new ol.Feature({
          geometry: new ol.geom.Point(ol.proj.fromLonLat([lng, lat]))
        })
      ]
    }));
    console.log(data)
  });    

})