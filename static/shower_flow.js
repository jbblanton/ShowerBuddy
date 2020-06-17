// """To Manage the Flow, but now in Java Script!"""


//  This is to toggle visibility between starting and playing a shower flow:
$(document).ready(function(){
  $('#start-shower').on('click', (evt) => {
    $("div.shower-action").show();
    $(".start-shower").hide();
  });  
});

//  This POSTS user_id from select menu; 
//    response includes Activities and Products as dictionaries:
$('#start-shower').on('click', (evt) => {
  evt.preventDefault();

  const formData = {
    user_id : $("#user-name :selected").val()
    };
    console.log(formData)
  
  $.post('/start_shower', formData, (response) => {
    if (response.success) {
    console.log(response)
    const activities = response.activities;
    console.log(activities)
    const products = response.products;
    console.log(products)
    runShowerFlow(activities, products)
    } else {
      alert(`Error: ${response.error}`);
    }
  });
});

// - List of activities names
// -activites[key]['name'] / ['description'] / ['video']


// let showerSeq = []
// for (const act of activities) {
//   showerSeq.push(act['name'])
// }

// - List of products names
// -products[key]['product_name'] / ['product_img'] / ['product_label_color']


// let showerProds = []
// for (const prod of products) {
//   showerProds.push(prod['product_name'])
// }


const runShowerFlow = (activities, products) => {

  const showerSeq = Object.keys(activities)

  const showerProds = Object.keys(products)

  for (const step of showerSeq) {
    const time = (1 * 60 * 1000) + ((60 * 1000) * showerSeq.indexOf(step))
    setTimeout(() => {$('h2#activity-name').html(activities[step]['name'].toUpperCase())}, time);
    setTimeout(() => {$('#activity-video').attr('src', activities[step]["video"])}, time);
   }

  for (const prod of showerProds) {
    const time = (1 * 60 * 1000) + ((60 * 1000) * showerProds.indexOf(prod))
    setTimeout(() => {$('#product-img').attr('src', products[prod]["product_img"])}, time);
    setTimeout(() => {$('product-label-color').attr('color', products[prod]['product_label_color'])})
  };



// function thisOne(list=myList, attributes=myAttr) {


//   for (const task of myList) {
//     const time = (1 * 60 * 1000) + ((60 * 1000) * myList.indexOf(task))
//     setTimeout(() => { $('h2#activity-name').html(task.toUpperCase()) }, time);
//     setTimeout(() => { $('#activity-video').attr('src', myAttr[task]["video"])}, time);
//     setTimeout(() => { $('#product-img').attr('src', myAttr[task]["img"])}, time);
//   }
// };

// thisOne is working!!!!!!!!!!!!!!!!!!

// Could I write a loop that generates these tasks? Time = x + 5 min
// var x = document.getElementById("counter");
// setTimeout(() => { x.innerHTML = "2 seconds" }, 2000);
// setTimeout(() => { x.innerHTML = "4 seconds" }, 4000);
// setTimeout(() => { x.innerHTML = "6 seconds" }, 6000);

// const myList = ["cat", "hippo", "fish", "rabbit"]
// // Need: dictionary of imgs for each item in list
// let myAttr = {
//   "cat": {"video": "https://giphy.com/embed/13CoXDiaCcCoyk", "img": "/static/img/bar_soap.png"},
//   "hippo": {"video": "https://giphy.com/embed/eN4E0uTymJpK0AOxHE", "img": "/static/img/lady_razor.png"},
//   "fish": {"video": "https://giphy.com/embed/FMeMqqNECWhos", "img": "/static/img/wash_hair.png"},
//   "rabbit": {"video": "https://giphy.com/embed/OR9y0z0vS0b3q", "img": "/static/img/shampoo2.png"}
// };
