// """To Manage the Flow, but now in Java Script!"""



// };
  // $('start-button').on('click', (evt) => {
  //   takeShower(flowID)
  // })



// This takes me to start_shower/2, but also gives a 404
// If I change to remove the { 'id' ..} it returns "TypeError: the view function did not return a valid response" and I see a 500 in the console
    let user_id = { 'id' : $("#user-name :selected").val() };
      console.log(user_id)
      // $.post('/start_shower', user_id);
    $("div.shower-action").show();
    $(".start-shower").hide();
 


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


