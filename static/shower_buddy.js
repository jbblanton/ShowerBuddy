
// Event handler to toggle the About info on/off the main screen (eliminating the need to have a separate About.html page)
// document.querySelector('#about-sb').addEventListener('click', (evt) => {
//   $("p.about").toggle(10);
// })

<<<<<<< HEAD
// const group = $("ol.shower-order").sortable({
//   group: 'shower-order',
//   isValidTarget: function ($item, container) {
//     if($item.is(".add"))
//       return true;
//     else
//       return $item.parent("ol")[0] == container.el[0];
//     // What is the point of this? Is it necessary to keep?
//   },
//   onDrop: function($item, container, _super) {
//     $('#serialize-output').text(
//       group.sortable("serialize").get().join("\n"));
//     _super($item, container);
//   },
//   serialize: function (parent, children, isContainer) {
//     return isContainer ? children.join() : parent.text();
//   },
//   tolerance: 6,
//   distance: 10
// });

// ? .json: 

// { 
//   "user-name": ,
//   "body": ,
//   "activites": [] ,
//   "caregiver-name": ,
//   "caregiver-phone": ,
//   "caregiver-email": ,
//   "caregiver-password": ,
//   "secret": 

// }

// const form = document.querySelector('form')[0];

// form.addEventListener('submit', (evt) => {
//   // lines to validate the info on the form;
//   // 1. confirm CG email does not already exist
//   // 2. verify valid phone number

//   if <something is innaccurate> {
//     evt.preventDefault();
//   }
// });

// const data.textContent = JSON.stringify(form);


// crud.create_caregiver(email=data.caregiver-email, telephone=data.caregiver-phone, password=data.caregiver-password);





// $('#create-user-form').on('submit', (evt) => {
//   // evt.preventDefault();

//   const formData = {
//     cgEmail: $('#caregiver-email').val(),
//     cgPass: $('#caregiver-password').val(),
//     cgCell: $('#caregiver-phone').val(),
//     userName: $('#user-name').val(),
//     userBody: $('.body-type').val()
//   };

//   console.log(formData);
//   console.log(formData.userName)

//   $.post('/create_user', formData, (response) => {
//     console.log(response)
//   })
// });
=======
// document.querySelector('#about-sb').addEventListener('click', (evt) => {
//   $("p.about").toggle(10);
// })






>>>>>>> af071d6... End of day 9
