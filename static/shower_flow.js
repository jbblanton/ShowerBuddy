// """To Manage the Flow, but now in Java Script!"""


// };
  // $('start-button').on('click', (evt) => {
  //   takeShower(flowID)
  // });



//  This is to toggle visibility between 
//    starting and playing a shower flow:
$(document).ready(function(){

  $('#start-shower').on('click', (evt) => {


// This takes me to start_shower/2, but also gives a 404
// If I change to remove the { 'id' ..} it returns "TypeError: the view function did not return a valid response" and I see a 500 in the console
    let user_id = { 'id' : $("#user-name :selected").val() };
      console.log(user_id)
      // $.post('/start_shower', user_id);
    $("div.shower-action").show();
    $(".start-shower").hide();

  });  

});

