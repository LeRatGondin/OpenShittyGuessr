// var map = L.map("map_1").fitWorld();
function sendData(value) {
  console.log(JSON.stringify({ lat: value.lat, lng: value.lng }));
  console.log(typeof value);
  $.ajax({
    url: "/process",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({ lat: value.lat, lng: value.lng }),
  });
}
window.addEventListener("load", function () {
  mapMarker = [];
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map_1);
  map_1.on("click", function (e) {
    if (mapMarker.length == 1) {
      mapMarker[0].remove();
      mapMarker.pop();
    }
    var marker = new L.marker(e.latlng).addTo(map_1);
    /*     console.log(e.latlng); */
    sendData(e.latlng);
    mapMarker.push(marker);
  });
});
