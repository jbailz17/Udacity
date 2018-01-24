var map;
var markers = [];
var largeInfoWindow;

function initMap() {

  var styles = [
    {
       "featureType": "all",
       "elementType": "all",
       "stylers": [
           {
               "invert_lightness": true
           },
           {
               "saturation": 10
           },
           {
               "lightness": 30
           },
           {
               "gamma": 0.5
           },
           {
               "hue": "#435158"
           }
       ]
   }
  ];

  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 35.6730185, lng: 139.4302008},
    zoom: 13,
    styles: styles,
    mapTypeControl: false
  });

  largeInfoWindow = new google.maps.InfoWindow({
    maxWidth: 200
  });

  var defaultIcon = makeMarkerIcon('ff003b');
  var highlightedIcon = makeMarkerIcon('168aff');

  for (var i = 0; i < locations.length; i++)
  {
    var position = locations[i].location;
    var title = locations[i].title;

    var marker = new google.maps.Marker({
      position: position,
      title: title,
      icon: defaultIcon,
      id: i
    });

    markers.push(marker);

    marker.addListener('click', function() {
      populateInfoWindow(this, largeInfoWindow);
    });

    marker.addListener('mouseover', function() {
      this.setIcon(highlightedIcon);
    });

    marker.addListener('mouseout', function() {
      this.setIcon(defaultIcon);
    });

  }

  showListings(markers);

}

function showListings(markers) {
  var bounds = new google.maps.LatLngBounds();

  for(var i = 0; i < markers.length; i++)
  {
    markers[i].setVisible(true);
    markers[i].setMap(map);
    bounds.extend(markers[i].position);
    toggleAnimation(markers[i]);
  }
  map.fitBounds(bounds);
}

function hideListings(markers) {
    for(var i = 0; i < markers.length; i++)
    {
      markers[i].setVisible(false);
    }
}

function makeMarkerIcon(markerColor) {
  var markerImage = new google.maps.MarkerImage(
    'http://chart.googleapis.com/chart?chst=d_map_spin&chld=1.15|0|'+ markerColor +
    '|40|_|%E2%80%A2',
    new google.maps.Size(21, 34),
    new google.maps.Point(0, 0),
    new google.maps.Point(10, 34),
    new google.maps.Size(21, 34)
  );
  return markerImage;
}

function toggleAnimation(marker) {
  if (marker.getAnimation() !== null) {
    marker.setAnimation(null);
  } else {
    marker.setAnimation(google.maps.Animation.BOUNCE);
    setTimeout(function() {
      marker.setAnimation(null);
    }, 2000);
  }
}

function populateInfoWindow(marker, infowindow) {
  if (infowindow.marker != marker) {
    infowindow.marker = marker;

    infowindow.addListener('closeclick', function(){
      infowindow.marker = null;
    });

    var wikiUrl = 'http://en.wikipedia.org/w/api.php?' +
     'action=opensearch&search=' + marker.title +
     '&prop=images&format=json&callback=wikiCallback';

    var wikirequestTimeout = setTimeout(function(){
      infowindow.setContent("<div><strong>" + marker.title + "</strong>" +
        "<br/><br/><p>failed to get wikipedia resources</p></div>");
    }, 8000);

    $.ajax({
      url: wikiUrl,
      dataType: "jsonp",
      success: function(response){
        var articleList = response[1];
        var summary = response[2][0];
        var article = articleList[0];
        var url = 'http://en.wikipedia.org/wiki/' + article

        infowindow.setContent('<div><a href="' + url + '"><strong>' +
          marker.title + '</strong></a><br/><br/>' +
          '<p>' + summary + '</p></div>');

        clearTimeout(wikirequestTimeout);
      }
    });

    infowindow.open(map, marker);
  }
}

function error() {
  alert('Unable to load the Google Maps Service.');
}
