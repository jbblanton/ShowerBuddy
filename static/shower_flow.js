// For the ABOUT paragraph on the homepage:

$("#about-button").on('click', function () {
  $("#about-text").toggle();
});


// This is to toggle visibility between dashboard and playing a shower flow:
$(document).ready(function(){
  $('#start-shower').on('click', (evt) => {
    $("div.shower-action").show();
    $(".start-shower").hide();
 })
});



// The SOS button; Upon click, a text is sent to caregiver 
//  & an alert pops on screen.
$('#HELP').on('click', (evt) => {
  const user_id = { user_id : $("#user-name :selected").val() };
  
  $.get('/send_help', user_id, (response) => {
    alert(response.msg);
  })
});



//  This POSTS user_id from select menu; 
//    response includes Activities and Products as dictionaries:
$('#start-shower').on('click', (evt) => {
  evt.preventDefault();

  const formData = {
    user_id : $("#user-name :selected").val(),
    };
  
  $.post('/start_shower', formData, (response) => {
    if (response.success) {
      // $( ).html(response.html)
      const activities = response.activities;
      const products = response.products;
      const duration = response.duration;
      runShowerFlow(activities, products, duration);
      exitShowerFlow(duration);

    } else {
      alert(`Error: ${response.error}`);
    }
  });
});


// Run the user's shower routine. 
//   Activity Name, Description, Video, Image, and Label color are
//    all sourced from the database and cycle through at a fixed pace.
// ...
// FUTURE FEATURES will include: 
//    - user interface ('done?' 'need more time?')
//      - alerts to caregiver if user does not progress to next step
const runShowerFlow = (activities, products, duration) => {

  const showerSeq = Object.keys(activities)
  const showerProds = Object.keys(products)
  
  const interval = ((showerSeq.length + 2) / duration) * 60000


// Set the timer to finish the shower:  
  let thisTime = duration * 60000
  setTimeout(() => {$('h2#activity-name').html('ALL DONE! DRY OFF')}, thisTime);
  setTimeout(() => {$('#activity-descr').html('Turn the water off. Carefully reach for your towel and dry your body, starting from your face, then shoulders and arms, and work your way down to your toes.  Be careful stepping out of the shower!')}, thisTime);
  setTimeout(() => {$('#activity-video').attr('src', "https://giphy.com/embed/kDBhX1Il2PZL66ljiL")}, thisTime);   
  setTimeout(() => {$('#product-img').attr('src', '')}, thisTime);

// Run the actual shower flow:
//    NOTE: This is assuming the length of both lists are equal; 
//      If & when caregivers can add images, 
//      this will not be true (eg. razor and shaving cream)  
  for (let idx = 0; idx <= showerSeq.length; idx++) {
    if (idx < showerSeq.length) {
      const time = interval + (60000 * idx)
      console.log(time / 1000)
      setTimeout(() => {$('h2#activity-name').html(activities[showerSeq[idx]]['name'].toUpperCase())}, time);
      setTimeout(() => {$('#activity-descr').html(activities[showerSeq[idx]]['description'])}, time);
      setTimeout(() => {$('#activity-video').attr('src', activities[showerSeq[idx]]["video"])}, time); 
      setTimeout(() => {$('#product-img').attr('src', products[showerProds[idx]]["image"])}, time);
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

