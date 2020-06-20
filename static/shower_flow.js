// For the ABOUT paragraph on the homepage:
$(document).ready(function(){
  $("#about-button").on('click', function () {
    $("#about-text").toggle();
  });
});  


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
      const duration = response.duration;
      runShowerFlow(activities, products, duration);
    } else {
      alert(`Error: ${response.error}`);
    }
  });
});


// The SOS button; Upon click, a text is sent to caregiver 
//  & an alert pops on screen.

$('#HELP').on('click', (evt) => {
  const user_id = { user_id : $("#user-name :selected").val() };
  
  $.get('/send_help', user_id, (response) => {
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
const runShowerFlow = (activities, products, duration) => {

  const showerSeq = Object.keys(activities)
  console.log(showerSeq)
  const showerProds = Object.keys(products)
  console.log(showerProds)
  
  console.log(duration)
  const interval = ((showerSeq.length + 2) / duration) * 60000
  console.log(interval)

// This is assuming the length of both lists are equal; 
//   If & when caregivers can add images, 
//   this will not be true (eg. razor and shaving cream)  
  for (let idx = 0; idx <= showerSeq.length; idx++) {
    if (idx < showerSeq.length) {
      const time = interval + (60000 * idx)
      setTimeout(() => {$('h2#activity-name').html(activities[showerSeq[idx]]['name'].toUpperCase())}, time);
      console.log(activities[showerSeq[idx]]['name'])
      setTimeout(() => {$('#activity-descr').html(activities[showerSeq[idx]]['description'])}, time);
      console.log(activities[showerSeq[idx]]['description'])
      setTimeout(() => {$('#activity-video').attr('src', activities[showerSeq[idx]]["video"])}, time);
      console.log(activities[showerSeq[idx]]["video"])    
      setTimeout(() => {$('#product-img').attr('src', products[showerProds[idx]]["image"])}, time);
      console.log(products[showerProds[idx]]["image"])
      // setTimeout(() => {$('product-label-color').attr('color', products[showerProds[idx]]['label_color'])});
    } else if (idx === showerSeq.length) {
      const time = interval + (60000 * showerSeq.length)
      setTimeout(() => {$('h2#activity-name').html('FINAL RINSE')}, time);
      setTimeout(() => {$('#activity-descr').html('RINSE all over; Make sure there\'s no more soap suds on your body or hair.')}, time);
      setTimeout(() => {$('#activity-video').attr('src', "https://giphy.com/embed/1tK61mF7P7x4I")}, time);   
      setTimeout(() => {$('#product-img').attr('src', '/static/img/shower_head2.png')}, time);
    }

  };
 
};
