// script.js

document.addEventListener('DOMContentLoaded', function() {
  const reservationForm = document.getElementById('reservationForm');
  const participantList = document.getElementById('participantList');

  if (reservationForm) {
      reservationForm.addEventListener('submit', function(event) {
          event.preventDefault(); // Prevent default form submission

          const nameInput = document.getElementById('name');
          const emailInput = document.getElementById('email');
          const expectationsInput = document.getElementById('expectations');

          // Using FormData is often easier when sending to PHP with $_POST
          const formData = new FormData();
          formData.append('name', nameInput.value.trim());
          formData.append('email', emailInput.value.trim());
          formData.append('expectations', expectationsInput.value.trim());

          // Basic client-side validation
          if (!formData.get('name') || !formData.get('email')) {
              alert('Please fill in your Full Name and Email Address.');
              return;
          }

          // --- The URL should point to your PHP script ---
          // Make sure your project is in htdocs, e.g., htdocs/chapteronecafe/
          // Then the URL will be http://localhost/chapteronecafe/register.php
          fetch('register.php', { // ADJUST THIS URL
              method: 'POST',
              body: formData, // Send as FormData, PHP will populate $_POST
              // No 'Content-Type' header needed when sending FormData;
              // the browser will set it correctly to 'multipart/form-data'
          })
          .then(response => {
              if (!response.ok) {
                  // Try to parse error as JSON, if not, use status text
                  return response.json().catch(() => {
                      throw new Error(`HTTP error! Status: ${response.status} - ${response.statusText}`);
                  }).then(errData => {
                      throw new Error(errData.message || `HTTP error! Status: ${response.status}`);
                  });
              }
              return response.json();
          })
          .then(data => {
              console.log('Server Response:', data);
              if (data.status === "success") {
                  alert(data.message || 'Registration successful!');
                  // Optionally, update UI or clear form
                  // const listItem = document.createElement('li');
                  // listItem.textContent = `Name: ${formData.get('name')}, Email: ${formData.get('email')}`;
                  // if (participantList) {
                  //     participantList.appendChild(listItem);
                  // }
                  reservationForm.reset();
              } else {
                  alert(`Registration failed: ${data.message || 'Unknown error'}`);
              }
          })
          .catch((error) => {
              console.error('Fetch Error:', error);
              alert(`An error occurred: ${error.message}`);
          });

          // --- EmailJS code can remain if you want to use it separately ---
          /*
          (function(){
            emailjs.init({ publicKey: "kDcfDCYEX1L5dZIzL" }); // Your EmailJS Public Key
          })();
          const templateParams = {
              from_name: formData.get('name'),
              from_email: formData.get('email'),
              message: `Expectations: ${formData.get('expectations') || 'N/A'}`
          };
          emailjs.send('YOUR_SERVICE_ID', 'YOUR_TEMPLATE_ID', templateParams)
              .then(function(response) {
                 console.log('EmailJS SUCCESS!', response.status, response.text);
              }, function(error) {
                 console.log('EmailJS FAILED...', error);
              });
          */
          // --- End of EmailJS part ---
      });
  }

  // Your existing ScrollReveal and other JS code can remain here
  // window.sr = ScrollReveal();
  // sr.reveal('.anime-left',{ /* ... */ });
});