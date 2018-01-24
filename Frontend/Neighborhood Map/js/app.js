var menu = false;

var locations = [
  {title: 'Tokyo Disneyland', location: {lat: 35.6328964, lng: 139.8782056}},
  {title: 'Haneda Airport', location: {lat: 35.5493932, lng: 139.7776499}},
  {title: 'Tokyo Tower', location: {lat: 35.6585805, lng: 139.7432442}},
  {title: 'Shiba Park', location: {lat: 35.6549376, lng: 139.7392289}},
  {title: 'Tokyo Imperial Palace', location: {lat: 35.6836585, lng: 139.7427268}}
]

var ViewModel = function() {
  var self = this;
  //self.listItems = ko.observableArray(locations);
  self.query = ko.observable('');

  this.toggleMenu = function() {
    var sideMenu = document.getElementById('listing-box');
    var header = document.getElementById('header');
    var map = document.getElementById('map');

    if (menu) {
      sideMenu.style.left = "-25%";
      map.style.left = "0%";
      header.style.left = "0%";
      menu = false;
    } else {
      sideMenu.style.left = "0%";
      map.style.left = "25%";
      header.style.left = "25%";
      menu = true;
    }
  }

  this.displayInfoWindow = function(location) {
    for (var i = 0; i < markers.length; i++) {
      if (markers[i].title == location.title) {
        populateInfoWindow(markers[i], largeInfoWindow);
      }
    }
  }

  this.showMarkers = function(location) {
    for (var i = 0; i < markers.length; i++) {
        if(markers[i].title == location.title) {
          markers[i].setVisible(true);
          toggleAnimation(markers[i]);
        }
    }
  }

  this.showCurrentLocation = function(clickedLocation) {
    hideListings(markers);
    self.showMarkers(clickedLocation);
    self.displayInfoWindow(clickedLocation);
  }

  this.showLocations = function() {
    hideListings(markers);
    showListings(markers);
  }

  this.listItems = ko.computed(function() {
    var q = self.query();
    hideListings(markers);
    return locations.filter(function(i) {
      if (i.title.toLowerCase().indexOf(q.toLowerCase()) >= 0) {
          self.showMarkers(i);
          return i.title;
      }
    });
  });
}

//ViewModel.query.subscribe(ViewModel.search);
ko.applyBindings(new ViewModel());
