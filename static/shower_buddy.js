
// Event handler to toggle the About info on/off the main screen (eliminating the need to have a separate About.html page)
// document.querySelector('#about-sb').addEventListener('click', (evt) => {
//   $("p.about").toggle(10);
// })



$("#about-button").on('click', function () {
  $("#about-text").toggle();
});  
  

