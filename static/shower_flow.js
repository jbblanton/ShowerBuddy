

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
    user_id : $("#flow-id :selected").val(),
    };
    console.log(formData.user_id)
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
  console.log(showerSeq)
  console.log(showerProds)
  
  const interval = (duration / (showerSeq.length + 2)) * 60 * 1000
//  const Testinterval = (duration / (showerSeq.length + 2)) * 1000

  console.log(interval)
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
      let time = interval + (interval * idx)
      console.log(time)
      console.log(activities[showerSeq[idx]]['name'])
//      let Testtime = Testinterval + (Testinterval * idx)
      setTimeout(() => {$('h2#activity-name').html(activities[showerSeq[idx]]['name'].toUpperCase())}, time);
      setTimeout(() => {$('#activity-descr').html(activities[showerSeq[idx]]['description'])}, time);
      setTimeout(() => {$('#activity-video').attr('src', activities[showerSeq[idx]]["video"])}, time); 
      setTimeout(() => {$('#product-img').attr('src', products[showerProds[idx]]["image"])}, time);
      // setTimeout(() => {$('product-label-color').attr('color', products[showerProds[idx]]['label_color'])});
    } else if (idx === showerSeq.length) {
      const endTime = (duration * 60 * 1000) - interval
      console.log('final rinse:')
      console.log(endTime)
//        const Testtime = Testinterval + (1000 * showerSeq.length)
        setTimeout(() => {$('h2#activity-name').html('FINAL RINSE')}, endTime);
        setTimeout(() => {$('#activity-descr').html('RINSE all over; Make sure there\'s no more soap suds on your body or hair.')}, endTime);
        setTimeout(() => {$('#activity-video').attr('src', "https://giphy.com/embed/1tK61mF7P7x4I")}, endTime);   
        setTimeout(() => {$('#product-img').attr('src', '/static/img/shower_head2.png')}, endTime);
    } else if (idx === showerSeq.length + 1) {
        let thisTime = duration * 60 * 1000
        console.log('all done:')
        console.log(thisTime)
//        let TestthisTime = duration * 1000
        setTimeout(() => {$('h2#activity-name').html('ALL DONE! DRY OFF')}, thisTime);
        setTimeout(() => {$('#activity-descr').html('Turn the water off. Carefully reach for your towel and dry your body, starting from your face, then shoulders and arms, and work your way down to your toes.  Be careful stepping out of the shower!')}, thisTime);
        setTimeout(() => {$('#activity-video').attr('src', "https://giphy.com/embed/kDBhX1Il2PZL66ljiL")}, thisTime);   
        setTimeout(() => {$('#product-img').attr('src', '')}, thisTime);
    } else if (idx === showerSeq.length + 2) {
        let thisTime = duration * 60 * 2000     
//        let TestthisTime = duration * 2000
        console.log('The End:')
        console.log(thisTime)
        setTimeout(() => {$('h2#activity-name').html('GREAT JOB!')},thisTime);
        setTimeout(() => {$('#activity-descr').hide()}, thisTime);
        setTimeout(() => {$('#activity-video').hide()}, thisTime);
        setTimeout(() => {$('#video-div').collapse()}, thisTime);
        setTimeout(() => {$('#product-img').hide()}, thisTime);
        setTimeout(() => {$("div.shower-ended").show()}, thisTime);
    }
  };
};





  // $("div.shower-action").hide()}, exitTime);
  // setTimeout(() => {$("div.shower-ended").show()}, exitTime);




  // ///// ////////// ////////////// ///////////////////////

// To enable drag and drop ordering of the shower events

// NONE of this really works. Sort of, and kind of, but it looks like shit and doesn't seem to add value to the project.




// let dragged;

// document.addEventListener("drag", function(evt) {

// }, false);

// document.addEventListener('dragstart', function(evt) {
//   dragged = evt.target;
//   evt.target.style.opacity = .5;
// }, false);

// document.addEventListener('dragend', function(evt) {
//   evt.target.style.opacity = "";
// }, false);

// document.addEventListener('dragover', function(evt) {
//   evt.preventDefault();
// }, false);

// document.addEventListener('dragenter', function(evt) {
//   if (evt.target.className == 'dropzone') {
//     // this color is too dark, but using it for now. RESTYLE!!
//     evt.target.style.background = "#272c67";  
//   }
// }, false);

// document.addEventListener('dragleave', function(evt) {
//   if (evt.target.className == 'dropzone') {
//     evt.target.style.background = "";
//   }
// }, false);

// document.addEventListener("drop", function(evt) {
//   evt.preventDefault();
//   if (evt.target.className == 'dropzone') {
//     evt.target.style.background = "";
//     dragged.parentNode.removeChild(dragged);
//     evt.target.appendChild(dragged);
//   }
// }, false);



//=> => https://www.youtube.com/watch?v=7HUCAYMylCQ

// dropzone.forEach(drop => {
//   drop.addEventListener('dragover', evt => {
//     evt.preventDefault();
//     const afterElement = getDragAfterElement(dropzone, evt.clientY);
//     const draggable = document.querySelector('.dragging');
//     if (afterElement == null) {
//       dropzone.appendChild(draggable);
//     } else {
//       dropzone.insertBefore(draggable, afterElement)
//     }
//   })
// });

// function getDragAfterElement(dropzone, y) {
//   const actions = [...dropzone.querySelectorAll('.draggable:not(.dragging)')]

//   return actions.reduce((closest, child) => {
//     const box = child.getBoundingClientRect();
//     const offset = y - box.top - box.height / 2
//     if (offset < 0 && offset > closest.offset) {
//       return { offset: offset, element: child }
//     } else {
//       return closest
//     }
//   }, { offset: Number.NEGATIVE_INFINITY }).element
// }



// // Add target element's id to the data transfer object
//   function dragstart_handler(evt) {
//     evt.dataTransfer.setData("text/plain", evt.target.id);
//   }

//   window.addEventListener('DOMContentLoaded', () => {
//     const element = document.getElementById('shampoo-act');
//     element.addEventListener('dragstart', dragstart_handler);
//   });


// // Add a drag image (choosing a black water droplet for now); 
// //    this may not be kept...
// function dragstart_handler(evt) {
//   let img = new Image();
//   img.src = '/static/css/black_drop.png'
//   evt.dataTransfer.setDragImage(img, 5, 5);
// }

// // To copy the item over, (alts are move and link)
// function dragstart_handler(evt) {
//   evt.dataTransfer.dropEffect = "copy";
// }

// function dragover_handler(evt) {
//   evt.preventDefault();
//   evt.dataTransfer.dropEffect = "copy"
// }

// function drop_handler(evt) {
//   evt.preventDefault();
//   const data = evt.dataTransfer.getData("text/plain");
//   evt.target.appendChild(document.getElementById(data));
// }