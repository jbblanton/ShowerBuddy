// For the ABOUT paragraph on the homepage:
$(document).ready(function(){
  $("#about-button").on('click', function () {
    $("#about-text").toggle();
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


// This is to toggle visibility between dashboard and playing a shower flow:
$(document).ready(function(){
  $('#start-shower').on('click', (evt) => {
    $("div.shower-action").show();
    $("#dashboard").toggle();
  });  
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
//      exitShowerFlow(duration);

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
  
//  const interval = (duration / (showerSeq.length + 2)) * 60 * 1000
  const Testinterval = (duration / (showerSeq.length + 2)) * 1000

// Set the timer to finish the shower:  
//  let thisTime = duration * 60 * 1000
  // let TestthisTime = duration * 1000
  // setTimeout(() => {$('h2#activity-name').html('ALL DONE! DRY OFF')}, TestthisTime);
  // setTimeout(() => {$('#activity-descr').html('Turn the water off. Carefully reach for your towel and dry your body, starting from your face, then shoulders and arms, and work your way down to your toes.  Be careful stepping out of the shower!')}, TestthisTime);
  // setTimeout(() => {$('#activity-video').attr('src', "https://giphy.com/embed/kDBhX1Il2PZL66ljiL")}, TestthisTime);   
  // setTimeout(() => {$('#product-img').attr('src', '')}, TestthisTime);
  // setTimeout(() => {$("div.shower-action").show()}, TestthisTime);


// Run the actual shower flow:
//    NOTE: This is assuming the length of both lists are equal; 
//      If & when caregivers can add images, 
//      this will not be true (eg. razor and shaving cream)  
  for (let idx = 0; idx <= showerSeq.length + 2; idx++) {
    if (idx < showerSeq.length) {
//      let time = interval + (interval * idx)
      let Testtime = Testinterval + (Testinterval * idx)
      setTimeout(() => {$('h2#activity-name').html(activities[showerSeq[idx]]['name'].toUpperCase())}, Testtime);
      setTimeout(() => {$('#activity-descr').html(activities[showerSeq[idx]]['description'])}, Testtime);
      setTimeout(() => {$('#activity-video').attr('src', activities[showerSeq[idx]]["video"])}, Testtime); 
      setTimeout(() => {$('#product-img').attr('src', products[showerProds[idx]]["image"])}, Testtime);
      // setTimeout(() => {$('product-label-color').attr('color', products[showerProds[idx]]['label_color'])});
    } else if (idx === showerSeq.length) {
//      const time = interval + (60000 * showerSeq.length)
        const Testtime = Testinterval + (1000 * showerSeq.length)
        setTimeout(() => {$('h2#activity-name').html('FINAL RINSE')}, Testtime);
        setTimeout(() => {$('#activity-descr').html('RINSE all over; Make sure there\'s no more soap suds on your body or hair.')}, Testtime);
        setTimeout(() => {$('#activity-video').attr('src', "https://giphy.com/embed/1tK61mF7P7x4I")}, Testtime);   
        setTimeout(() => {$('#product-img').attr('src', '/static/img/shower_head2.png')}, Testtime);
    } else if (idx === showerSeq.length + 1) {
//  let thisTime = duration * 60 * 1000
        let TestthisTime = duration * 1000
        setTimeout(() => {$('h2#activity-name').html('ALL DONE! DRY OFF')}, TestthisTime);
        setTimeout(() => {$('#activity-descr').html('Turn the water off. Carefully reach for your towel and dry your body, starting from your face, then shoulders and arms, and work your way down to your toes.  Be careful stepping out of the shower!')}, TestthisTime);
        setTimeout(() => {$('#activity-video').attr('src', "https://giphy.com/embed/kDBhX1Il2PZL66ljiL")}, TestthisTime);   
        setTimeout(() => {$('#product-img').attr('src', '')}, TestthisTime);
    } else if (idx === showerSeq.length + 2) {
//      PUT IN A REAL TIME HERE!!      
        let TestthisTime = duration * 2000
        setTimeout(() => {$('h2#activity-name').html('GREAT JOB!')}, TestthisTime);
        setTimeout(() => {$('#activity-descr').hide()}, TestthisTime);
        setTimeout(() => {$('#activity-video').hide()}, TestthisTime);
        setTimeout(() => {$('#product-img').hide()}, TestthisTime);
        setTimeout(() => {$("div.shower-ended").show()}, TestthisTime);
    }
  };
};






// This button is to edit an existing user flow:
// TO DO: you know what you need to do





  // $("div.shower-action").hide()}, exitTime);
  // setTimeout(() => {$("div.shower-ended").show()}, exitTime);