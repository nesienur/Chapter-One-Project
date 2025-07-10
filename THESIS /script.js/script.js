document.addEventListener('DOMContentLoaded', function () {
    emailjs.init("BxxlzhhPWsSGtp_V2");


  const reservationForm = document.getElementById('reservationForm');

  if (reservationForm) {
    reservationForm.addEventListener('submit', function (event) {
      event.preventDefault();

      const name = document.getElementById('name').value.trim();
      const email = document.getElementById('email').value.trim();
      const expectations = document.getElementById('expectations').value.trim() || "N/A";
      const whichEvent = document.getElementById('which_event_will_you_be_attending').value.trim() || null;

      if (!name || !email) {
        alert("Please fill in the name and email fields.");
        return;
      }

      const formData = new FormData();
      formData.append('name', name);
      formData.append('email', email);
      formData.append('which_event_will_you_be_attending', whichEvent);
      formData.append('expectations', expectations);

      // ✅ Veritabanına kayıt
      fetch('register.php', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === "success") {
          alert(data.message || 'Registration successful!');

          // ✅ QR kodu oluştur
          const qrText = `${name} - ChapterOneCafe30`;
          const qrImageUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(qrText)}`;


          // ✅ Email gönder
          emailjs.send("service_434ga9w", "template_qc1gz1i", {
            user_name: name,
            to_email: email,
            email: email, 
            expectations: expectations,
            which_event_will_you_be_attending: whichEvent,
            qr_code: qrImageUrl
          })
          .then(function () {
            console.log("✅ Email sent.");
            reservationForm.reset();
          })
          .catch(function (error) {
            console.error("❌ EmailJS error:", error);
            alert("❌ Email could not be sent.");
          });

        } else {
          alert("❌ Registration failed: " + data.message);
        }
      })
    });
  }
});
