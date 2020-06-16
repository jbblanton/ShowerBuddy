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



// Could I write a loop that generates these tasks? Time = x + 5 min
// var x = document.getElementById("counter");
// setTimeout(() => { x.innerHTML = "2 seconds" }, 2000);
// setTimeout(() => { x.innerHTML = "4 seconds" }, 4000);
// setTimeout(() => { x.innerHTML = "6 seconds" }, 6000);

const myList = ["cat", "hippo", "fish", "rabbit"]
// Need: dictionary of imgs for each item in list
let myAttr = {
  "cat": {"video": "https://giphy.com/embed/13CoXDiaCcCoyk", "img": "/static/img/bar_soap.png"},
  "hippo": {"video": "https://giphy.com/embed/eN4E0uTymJpK0AOxHE", "img": "/static/img/lady_razor.png"},
  "fish": {"video": "https://giphy.com/embed/FMeMqqNECWhos", "img": "/static/img/wash_hair.png"},
  "rabbit": {"video": "https://giphy.com/embed/OR9y0z0vS0b3q", "img": "/static/img/shampoo2.png"}
};

function thisOne(list=myList, attributes=myAttr) {


  for (const task of myList) {
    const time = (1 * 60 * 1000) + ((60 * 1000) * myList.indexOf(task))
    setTimeout(() => { $('h2#activity-name').html(task.toUpperCase()) }, time);
    setTimeout(() => { $('#activity-video').attr('src', myAttr[task]["video"])}, time);
    setTimeout(() => { $('#product-img').attr('src', myAttr[task]["img"])}, time);
  }
};

// thisOne is working!!!!!!!!!!!!!!!!!!
