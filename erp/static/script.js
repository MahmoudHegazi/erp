window.addEventListener('DOMContentLoaded', (event) => {
const checkin_form = document.getElementById('checkin_form');
const checkout_form = document.getElementById('checkout_form');
const history_form = document.getElementById('history_form');


// Check in Form AJAX
checkin_form.onsubmit = function(e) {
  let checkin_value = document.getElementById('employee_code_in');
  e.preventDefault();
  fetch('/checkin', {
    method: 'POST',
    body: JSON.stringify({
      'code': checkin_value.value
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  }).then(function(response) {
       return response.json();
   }).then(function(jsonres){
      console.log(jsonres);
      let message = jsonres['message'];
      let html_message =
      `<div class="alert alert-info"><strong> ${message} </strong><span class="closebtn" style="float:right;background-color:red;color:white;padding:2px;width:25px;text-align:center;margin-bottom:26px;font-size:1em;cursor:pointer;font-weight:bold;border:2px solid white;border-radous:8%;">&times;</span></div>`;
      let get_container = document.getElementById('notification_message');
      get_container.innerHTML = html_message;
      console.log(jsonres);
      var close = document.getElementsByClassName("closebtn");
      var i;

      for (i = 0; i < close.length; i++) {
      close[i].onclick = function(){
      var div = this.parentElement;
      div.style.opacity = "0";
      setTimeout(function(){ div.style.display = "none"; }, 600);
      }
      }

   });
}


// Check out Form AJAX
checkout_form.onsubmit = function(e) {
  let checkout_value = document.getElementById('employee_code_out');
  e.preventDefault();
  fetch('/checkout', {
    method: 'POST',
    body: JSON.stringify({
      'code': checkout_value.value
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  }).then(function(response) {
       return response.json();
   }).then(function(jsonres){
     let message = jsonres['message'];
     let html_message = `<div class="alert alert-info"><strong> ${message} </strong><span class="closebtn" style="float:right;background-color:red;color:white;padding:2px;width:25px;text-align:center;margin-bottom:26px;font-size:1em;cursor:pointer;font-weight:bold;border:2px solid white;border-radous:8%;">&times;</span></div>`;
     let get_container = document.getElementById('notification_message');
     get_container.innerHTML = html_message;
     console.log(jsonres)
     var close = document.getElementsByClassName("closebtn");
     var i;

     for (i = 0; i < close.length; i++) {
     close[i].onclick = function(){
     var div = this.parentElement;
     div.style.opacity = "0";
     setTimeout(function(){ div.style.display = "none"; }, 600);
     }
     }
   });
}



// Get History Form AJAX


})
