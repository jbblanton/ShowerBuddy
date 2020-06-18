// """To Manage the Flow, but now in Java Script!"""


// This is to toggle visibility between starting and playing a shower flow:
$(document).ready(function(){
  $('#start-shower').on('click', (evt) => {
    $("div.shower-action").show();
    $(".start-shower").hide();
 })
});



//  This POSTS user_id from select menu; 
//    response includes Activities and Products as dictionaries:
$('#start-shower').on('click', (evt) => {
  evt.preventDefault();

  const formData = {
    user_id : $("#user-name :selected").val(),
    };
  console.log(formData.user_id)
  
  $.post('/start_shower', formData, (response) => {
    if (response.success) {
      // $( ).html(response.html)
      const activities = response.activities;
      console.log(activities)
      const products = response.products;
      console.log(products)
      runShowerFlow(activities, products);
    } else {
      alert(`Error: ${response.error}`);
    }
  });
});


// The SOS button; TO DO: Personalize with the user's name
$('#HELP').on('click', (evt) => {
  $.get('/send_help', (response) => {

      alert(response.msg);
  })
});




// Run the user's shower routine. 
//   Activity Name, Description, Video, Image, and Label color are
//    all sourced from the database and cycle through at a fixed pace.
// ...
// FUTURE FEATURES will include: 
//    - variable cycle speeds (slow/med/fast)
//    - user interface ('done?' 'need more time?')
//      - alerts to caregiver if user does not progress to next step
const runShowerFlow = (activities, products) => {

  const showerSeq = Object.keys(activities)
  console.log(showerSeq)
  const showerProds = Object.keys(products)
  console.log(showerProds)

// This is assuming the length of both lists are equal; 
//   If & when caregivers can add images, 
//   this will not be true (eg. razor and shaving cream)  
  for (let idx = 0; idx < showerSeq.length; idx++) {
    const time = (1 * 30 * 1000) + ((30 * 1000) * idx)
    setTimeout(() => {$('h2#activity-name').html(activities[showerSeq[idx]]['name'].toUpperCase())}, time);
    setTimeout(() => {$('#activity-descr').html(activities[showerSeq[idx]]['description'])}, time);
    setTimeout(() => {$('#activity-video').attr('src', activities[showerSeq[idx]]["video"])}, time);
    setTimeout(() => {$('#product-img').attr('src', products[showerProds[idx]]["image"])}, time);
    // setTimeout(() => {$('product-label-color').attr('color', products[showerProds[idx]]['label_color'])});
  }
};
