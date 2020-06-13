// """To Manage the Flow, but now in Java Script!"""

// function createShowerFlow(flowID) {
//   // Use this function to make a list of activities for a given user"""
//     // # Shower Flow = { step_num : 
//     // #                 activity_id:
//     // #                     activity_name:
//     // #                     description:
//     // #                     video:  

//   const activities = [];
//   return activities
// }

// function createProductList(flowID) {
//   // Use this to make a list of the products needed during a given flow

//       // Product = { product_id:
//       //               product_image:
//       //               product_name:
//       //               product_color_label:
//       //           }

//   const products = [];
//   return products
// }


//  This is to toggle visibility between 
//    starting and playing a shower flow:
$(document).ready(function(){

  $('#start-shower').on('click', (evt) => {

    $("div.shower-action").show();
    $(".start-shower").hide();
  });  

});