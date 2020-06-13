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

// function takeShower(flowID) {
//   // Here is the actual shower flow.

//       // Activities list will populate from the user's flow.
//       // If statements control the order of the flow, and each activity is 
//       // removed after completion.
//       // Initial Rinse and Final Rinse are universal steps.

//   const activities = createShowerFlow(flowID);

//   let showerActive === true;

//   initialRinse();

//   while showerActive {

//     if (activities.includes("shampoo")) {
//       shampooHair(activityID, productID)
//       const index = activities.indexOf("shampoo")
//       if (index > -1) {activities.splice(index, 1) };
//       continue
//     };

//     if (activities.includes("conditioner")) {
//       conditionHair(activityID, productID)
//       const index = activities.indexOf("conditioner")
//       if (index > -1) {
//         activities.splice(index, 1) };
//       continue
//     };

//   };

// };
  // $('start-button').on('click', (evt) => {
  //   takeShower(flowID)
  // });




//  This is to toggle visibility between 
//    starting and playing a shower flow:
$(document).ready(function(){

  $('#start-shower').on('click', (evt) => {

    $("div.shower-action").show();
    $(".start-shower").hide();
  });  

});






function testList() {

  let myList = ["cat", "dog", "fish"]

  let active = true;

  startAction(0);
  console.log("started");

  while (active) {

    if (myList.includes("dog")) {
      firstFunc(1)
      console.log("dog")
      const index = myList.indexOf("dog")
      if (index > -1) {
        myList.splice(index, 1) }
      continue
      };

    if (myList.includes("cat")) {
      secondFunc(2)
      console.log("cat")
      const index = myList.indexOf("cat")
      if (index > -1) {
        myList.splice(index, 1)
      }
      continue
    };

    if (myList.includes("horse")) {
      thirdFunc(3)
      console.log("horse")
      const index = myList.indexOf("horse")
      if (index > -1) {
        myList.splice(index, 1)
      }
      continue
    };

    active = finalTest()
    console.log("complete");

  };    
};

function startAction(n){

  // Update activity_name in the h1
  $('activity-name').html(activity_name);

  // Update activity_video in embed
  $('activity-video').attr('src', activity_video);

  // Update product_img in img
  $('product-img').attr('src', product_img);

  // Reset progress bar
  
  // Reset timer (together)

};

function firstFunc() {
  return "done"
};

function secondFunc() {
  return "done"
};

function thirdFunc() {
  return "done"
};

function finalTest() {
  return false
};

