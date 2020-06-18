
<<<<<<< HEAD
// Event handler to toggle the About info on/off the main screen (eliminating the need to have a separate About.html page)
// document.querySelector('#about-sb').addEventListener('click', (evt) => {
//   $("p.about").toggle(10);
// })

=======
>>>>>>> 4ecf779... WOO! Shower flow is functional!


// For the ABOUT paragraph on the homepage:
$("#about-button").on('click', function () {
  $("#about-text").toggle();
});  
  

<<<<<<< HEAD
=======
// //  This POSTS user_id from select menu; 
// //    response includes Activities and Products as dictionaries:
// $('#start-shower').on('click', (evt) => {
//   evt.preventDefault();

//   const formData = {
//     user_id : $("#user-name :selected").val()
//     };

  
//   $.post('/start_shower', formData, (response) => {
//     if (response.success) {
//       $(this).html(response.html)
//     const activities = response.activities;
//     console.log(activities)
//     const products = response.products;
//     console.log(products)
//     runShowerFlow(activities, products)
//     } else {
//       alert(`Error: ${response.error}`);
//     }
//   });
// });
>>>>>>> 4ecf779... WOO! Shower flow is functional!
