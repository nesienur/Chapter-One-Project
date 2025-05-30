
document.getElementById('reservationForm').addEventListener('submit', async function(event) {
  event.preventDefault(); // Formun normal submitini engelle

  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const expectations = document.getElementById('expectations').value;

  const data = { name, email, expectations };

  try {
    const response = await fetch('/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if(response.ok) {
      alert('Kayıt başarılı! Teşekkürler.');
      this.reset(); // Formu temizle
    } else {
      alert('Kayıt başarısız: ' + (result.message || 'Bilinmeyen hata'));
    }

  } catch (error) {
    alert('Sunucuya bağlanırken hata oluştu.');
    console.error(error);
  }
});
