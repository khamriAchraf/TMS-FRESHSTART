function convertTime(sec) {
    var hours = Math.floor(sec/3600);
    (hours >= 1) ? sec = sec - (hours*3600) : hours = '00';
    var min = Math.floor(sec/60);
    (min >= 1) ? sec = sec - (min*60) : min = '00';
    (sec < 1) ? sec='00' : void 0;

    (min.toString().length == 1) ? min = '0'+min : void 0;
    (sec.toString().length == 1) ? sec = '0'+sec : void 0;

    return hours+'h  '+min+'min';
}



function computeTotal(result){
    let totalDistance=0;
    let totalDuration=0;
    const myroute = result.routes[0];
    for (let i = 0; i < myroute.legs.length; i++) {
        totalDistance += myroute.legs[i].distance.value;
        totalDuration += myroute.legs[i].duration.value;
    }
    totalDistance=Math.round(totalDistance/1000)+" km"
    totalDuration=convertTime(totalDuration)

    distanceHTML=document.getElementById('total-distance')
    distanceHTML.innerHTML="<hr><b>Distance totale : </b>"+totalDistance

    durationHTML=document.getElementById('total-duration')
    durationHTML.innerHTML="<b>Durée totale estimée : </b>"+totalDuration +"<hr>"

}

var alertPlaceholder = document.getElementById('liveAlertPlaceholder')

function alert(message, type) {
  var wrapper = document.createElement('div')
  wrapper.innerHTML = '<div id="alert" class="alert alert-' + type + ' alert-dismissible" role="alert">' + message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'
  if (!document.getElementById("alert")){
      alertPlaceholder.append(wrapper)
  }
}
counter=0
function initMap() {
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer({
        draggable: true,
    });
    // On directions changed compute new totals and send alert
    directionsRenderer.addListener("directions_changed", () => {
        const directions = directionsRenderer.getDirections();

        if (directions) {
            if (counter>0){
                alert('<b>Attention ! </b>Vous avez modifié manuellement la route. La tournée risque d\'être plus longue.', 'warning');
            };
            counter++;
            }
          computeTotal(directions);


    });
    const map = new google.maps.Map(document.getElementById("map"), {
        mapId:"5603b8170f929",
        zoom: 6,
        center: { lat: 31.580681, lng: -6 },
    });

    directionsRenderer.setMap(map);
    document.getElementById("show").addEventListener("click", () => {
      calculateAndDisplayRoute(directionsService, directionsRenderer);
    });
  }

  function calculateAndDisplayRoute(directionsService, directionsRenderer) {
    const waypts = [];

    for (let i = 1; i < ordered_cities.length-1; i++) {
        waypts.push({
          location: ordered_cities[i],
          stopover: true,
        });
    }
    directionsService
      .route({
        origin: ordered_cities[0],
        destination: ordered_cities[0],
        waypoints: waypts,
        optimizeWaypoints: false,
        travelMode: google.maps.TravelMode.DRIVING,
      })
      .then((response) => {
        directionsRenderer.setDirections(response);
        directionsRenderer.setOptions({
            polylineOptions: {
                strokeColor: '#faea73',
                strokeWeight:'5'
            },
        });
        console.log(response.routes.legs);
        const route = response.routes[0];
        const summaryPanel = document.getElementById("directions-panel");

        summaryPanel.innerHTML = "";
        // For each route, display summary information.
        for (let i = 0; i < route.legs.length; i++) {
          const routeSegment = i + 1;

          summaryPanel.innerHTML +=
            "<b>Segment de route : " + routeSegment + "</b><br>";
          summaryPanel.innerHTML += route.legs[i].start_address + " à ";
          summaryPanel.innerHTML += route.legs[i].end_address + "<br>";
          summaryPanel.innerHTML += route.legs[i].distance.text + "<br>";
          summaryPanel.innerHTML += route.legs[i].duration.text + "<br><br>";
        }
        computeTotal(response);

      })
      .catch((e) => window.alert("Directions request failed due to " + e,'danger'));
  }

