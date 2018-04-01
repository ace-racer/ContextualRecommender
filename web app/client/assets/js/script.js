$(document).ready(function($) {

	$('.card__share > a').on('click', function(e){ 
		e.preventDefault() // prevent default action - hash doesn't appear in url
   		$(this).parent().find( 'div' ).toggleClass( 'card__social--active' );
		$(this).toggleClass('share-expanded');
    });
  

  $.ajax({
    url: 'http://127.0.0.1:5000/streams/neighbors/580',
    dataType: 'json',
    headers: {"Access-Control-Allow-Origin": '*'},
    crossDomain: true,
    jsonpCallback: 'callback',
    type: 'GET',
    success: function (data) {
        console.log(data);
    }
});
  

  
});
 