// Added via Bootstrap, to enable hover-over tool-tips:
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})


// For the ABOUT paragraph on the homepage:
$(document).ready(function(){
  $("#about-button").on('click', function () {
    $("#about-text").toggle();
  });
});  


// Get flow_id for editing; This is on the edit_user page
$('#edit-flow').on('click', (evt) => {
  (evt).preventDefault();
  const flow_id = $("#flow-id :selected").val();

  $.get(`/edit_user/${flow_id}`, (response) => {

    if (response.success) {
      const activities = response.activities;
      const title = response.title;
      const duration = response.duration;

      fillEditForm(title, activities, duration);
    }
  })
});


const fillEditForm = (title, activities, duration) => {

  $('#upd-flow-title').replaceWith(`<input id="upd-flow-title" type="text" data-toggle="tooltip" data-placement="right" title="Try something like 'Sunday', 'quick-wash', etc. to help you distinguish different routines for the same person.  Hint: the default is 'daily'" name="flow-name" placeholder='${title}'>`);

  for (event of activities) {

    $(`#${event}`).attr("checked", true);
  };

  $(`#${duration}`).attr("checked", true);
};


$('#update-user-btn').on('click', (evt) => {
  evt.preventDefault();

  let activities = [];
  $.each($('[name="upd-activity"]:checked'), function() {
    activities.push($(this).val());
  });

  const formData = {
    flow_id: $("#flow-id :selected").val(),
    flow_title : $('#upd-flow-title').val(),
    f_activities : activities,
    duration : $('[name="upd-duration"]:checked').val(),
    }

  $.get('/submit_edits', formData, (response) => {
    alert('The updates have been made!')
  })
});


// The SOS button; Upon click, a text is sent to caregiver 
//  & an alert pops on screen.
$('#HELP').on('click', (evt) => {
  const flow_id = { flow_id : $("#flow-id :selected").val() };

  $.get('/send_help', flow_id, (response) => {
    alert(response.msg);
  })
});


// This is to toggle visibility between dashboard and playing a shower flow:
$(document).ready(function(){
  $('#start-shower').on('click', (evt) => {
    $("#shower-action").show();
    $("#dashboard").toggle();
  });  
});


//  This POSTS user_id from select menu; 
//    response includes Activities and Products as dictionaries:
$('#start-shower').on('click', (evt) => {
  evt.preventDefault();

  const formData = {
    user_id : $("#flow-id :selected").val(),
    };

  $.post('/start_shower', formData, (response) => {
    
    if (response.success) {

      const activities = response.activities;
      const products = response.products;
      const duration = response.duration;
      runShowerFlow(activities, products, duration);

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

// For the demo:
  const demoInterval = (duration / (showerSeq.length + 2)) * 2000 

// Run the actual shower flow:
//    NOTE: This is assuming the length of both lists are equal; 
//      If & when caregivers can add images, 
//      this will not be true (eg. razor and shaving cream)  
  for (let idx = 0; idx <= (showerSeq.length + 2); idx++) {
    if (idx < showerSeq.length) {
//      let time = interval + (interval * idx)
      let demoTime = demoInterval + (demoInterval * idx)

      setTimeout(() => {$('h2#activity-name').html(activities[showerSeq[idx]]['name'].toUpperCase())}, demoTime);
      setTimeout(() => {$('#activity-descr').html(activities[showerSeq[idx]]['description'])}, demoTime);
      setTimeout(() => {$('#activity-video').attr('src', activities[showerSeq[idx]]["video"])}, demoTime); 
      setTimeout(() => {$('#product-img').attr('src', products[showerProds[idx]]["image"])}, demoTime);
      // setTimeout(() => {$('product-label-color').attr('color', products[showerProds[idx]]['label_color'])});
    } else if (idx === showerSeq.length) {
//      const endTime = (duration * 60 * 1000) - interval
      const demoFR = (duration * 2000) - demoInterval 

        setTimeout(() => {$('h2#activity-name').html('FINAL RINSE')}, demoFR);
        setTimeout(() => {$('#activity-descr').html('RINSE all over; Make sure there\'s no more soap suds on your body or hair.')}, demoFR);
        setTimeout(() => {$('#activity-video').attr('src', "https://giphy.com/embed/1tK61mF7P7x4I")}, demoFR);   
        setTimeout(() => {$('#product-img').attr('src', '/static/img/shower_head2.png')}, demoFR);
    } else if (idx === showerSeq.length + 1) {
//        let thisTime = duration * 60 * 1000
        let demoDry = duration * 2000

        setTimeout(() => {$('h2#activity-name').html('ALL DONE! DRY OFF')}, demoDry);
        setTimeout(() => {$('#activity-descr').html('Turn the water off. Carefully reach for your towel and dry your body, starting from your face, then shoulders and arms, and work your way down to your toes.  Be careful stepping out of the shower!')}, demoDry);
        setTimeout(() => {$('#activity-video').attr('src', "https://giphy.com/embed/kDBhX1Il2PZL66ljiL")}, demoDry);   
        setTimeout(() => {$('#product-img').attr('src', '/static/img/red_towel.png')}, demoDry);
    } else if (idx === showerSeq.length + 2) {
//        let thisTime = (duration + 2) * 60 * 1000     
        let demoExit = (duration  + 2) * 2000

        setTimeout(() => {$('h2#activity-name').html('GREAT JOB!')},demoExit);
        setTimeout(() => {$('#activity-descr').hide()}, demoExit);
        setTimeout(() => {$('#vid-img-block').hide()}, demoExit);
        // setTimeout(() => {$('#video-div').collapse()}, TestthisTime);
        // setTimeout(() => {$('#product-img').collapse()}, TestthisTime);
        setTimeout(() => {$("#shower-ended").show()}, demoExit);
    }
  };
};
