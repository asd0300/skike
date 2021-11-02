let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 25.0336962, lng: 121.5643673 },
    zoom: 8,
  });

  var polylinePathPoints = [
    { lat: 25.0336962, lng: 121.5643673 },
    { lat: 25.033755, lng: 121.565412 },
    { lat: 25.031985, lng: 121.56538 },
    { lat: 25.032083, lng: 121.561324 },
  ];
  var polylinePath = new google.maps.Polyline({
    path: polylinePathPoints,
    geodesic: true,
    strokeColor: "#008800",
    strokeOpacity: 0.8,
    strokeWeight: 20,
    editable: true,
    geodesic: false,
    draggable: true,
  });

  polylinePath.setMap(map);

  polylinePath.addListener("drag", function () {
    this.setOptions({
      strokeColor: "#ff0000",
    });
  });

  polylinePath.addListener("dragend", function () {
    this.setOptions({
      strokeColor: "#008800",
    });
  });
}
