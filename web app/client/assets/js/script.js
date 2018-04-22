$( window ).on( "load", function() {

	$('.card__share > a').on('click', function(e){ 
		e.preventDefault() // prevent default action - hash doesn't appear in url
   		$(this).parent().find( 'div' ).toggleClass( 'card__social--active' );
		$(this).toggleClass('share-expanded');
    });
  
//      $(".card").on( "click", function() {
//          console.log("clicked");
//          console.log($(this));
//          var one = $(this).find('.streamid').find('a').html();
//          console.log(one);
//          var url = "main.html"+ '?streamid='+ one;
//          window.location.href = url;
//        
//               
//        });
//  $.ajax({
//    url: 'http://127.0.0.1:5000/streams/neighbors/1104',
//    dataType: 'json',
//    headers: {"Access-Control-Allow-Origin": '*'},
//    crossDomain: true,
//    jsonpCallback: 'callback',
//    type: 'GET',
//    success: function (data) {
//        console.log(data.Target.tags[0],data.Target.tags[1],data.Target.tags[2],data.Target.tags[3]);
//      
//      console.log("Neighbour "+ data.Neighbors[0].tags[0] + data.Target.tags);
//       
//     for (i = 0; i < data.Target.tags.length; i++) {  
//        for (j = 0; j < data.Neighbors.length; j++) {  
//          for (k = 0; k < data.Neighbors[j].tags.length; k++) {  
//            if(data.Target.tags[i] === data.Neighbors[j].tags[k]){
//              var htmltext = $(".related-stream .tags h6 a").html();
//              
//              $('.related-stream .tags').find('h6').each(function() {
//                  console.log($(this).html());
//                if($(this).find('a').html() ===data.Target.tags[i] ){
//                  $(this).css("background-color", "#9b59b6");
//                }
//              });
//              
//              
//              //console.log(htmltext);
//              //$(".related-stream .tags h6").css("background-color", "yellow");
//              console.log("gsdhd");
//            }
//          }
//            
//        }
//     }
//      
//    $('#view-card').click(function(e){
//      $('.card-names').toggle();
//                
//     
//      
//    }); 
//      
//      
//        
//      
//    }
//});
  

  
});
 