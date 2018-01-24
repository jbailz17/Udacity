
function loadData() {

    var $body = $('body');
    var $wikiElem = $('#wikipedia-links');
    var $nytHeaderElem = $('#nytimes-header');
    var $nytElem = $('#nytimes-articles');
    var $greeting = $('#greeting');

    // clear out old data before new request
    $wikiElem.text("");
    $nytElem.text("");

    // load streetview
    var street = $('#street').val();
    var city = $('#city').val();
    var address = street + ',' + city;

    $greeting.text('So, you want to live at ' + address + '?');

    var streetviewUrl = 'http://maps.googleapis.com/maps/api/';
    streetviewUrl += 'streetview?size=600x300&location=' + address + '';

    $body.append('<img class="bgimg" src="' + streetviewUrl + '">')

    // YOUR CODE GOES HERE!
    var nytimesUrl = 'http://api.nytimes.com/svc/search/v2/';
    nytimesUrl += 'articlesearch.json?q=' + city + '&sort=newest&api-'
    nytimesUrl += 'key=521debc074704bfbb9ad4e3c27423ce7'

    $.getJSON(nytimesUrl, function(data){
      $nytHeaderElem.text('New Yourk Times Articles About ' + city);
      articles = data.response.docs;
      for (var i = 0; i < articles.length; i++){
        var article = articles[i];
        $nytElem.append('<li class="article">'+
            '<a href="'+article.web_url+'">'+article.headline.main+
            '</a>'+'<p>'+article.snippet+'</p>'+'</li>');
      }
    }).error(function(e){
      $nytHeaderElem.text('New York Times Articles Could Not Be Loaded');
    });

    var wikiUrl = 'http://en.wikipedia.org/w/api.php?';
    wikiUrl += 'action=opensearch&search=' + city ;
    wikiUrl += '&format=json&callback=wikiCallback';

    var wikirequestTimeout = setTimeout(function(){
      $wikiElem.text("failed to get wikipedia resources");
    }, 8000);

    $.ajax({
      url: wikiUrl,
      dataType: "jsonp",
      success: function(response){
        var articleList = response[1];

        for (var i = 0; i < articleList.length; i++) {
          article = articleList[i];
          var url = 'http://en.wikipedia.org/wiki/' + article;
          $wikiElem.append('<li><a href="' + url +'">' +
              article + '</a></li>');
        }

        clearTimeout(wikirequestTimeout);
      }
    });

    return false;
};

$('#form-container').submit(loadData);
