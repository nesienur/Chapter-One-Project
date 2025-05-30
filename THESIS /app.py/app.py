from flask import Flask, request, render_template, redirect, flash, url_for, jsonify
from flask_mail import Mail, Message
import mysql.connector # MySQL veritabanı bağlantısı için gerekli
import os # Ortam değişkenlerini kullanmak için

app = Flask(__name__)
# Flask'ın oturumları ve flash mesajları için gizli anahtar.
# Üretim ortamında daha karmaşık ve güvenli bir anahtar kullanmalısın.
app.secret_key = 'your_super_secret_key_here' 

# Flask-Mail yapılandırması
# E-posta gönderme ayarları. Kendi Gmail hesabın ve uygulama şifren olmalı.
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='your_email@gmail.com',        # Kendi Gmail adresini buraya yaz
    MAIL_PASSWORD='wjak lqyn tqjh nhpx',      # Gmail uygulama şifreni buraya yaz (uygulama şifresi, normal şifre değil)
)
mail = Mail(app)

# MySQL Veritabanı Yapılandırması
# Veritabanı bağlantı bilgileri. Güvenlik için ortam değişkenlerinden çekmek en iyisidir.
# Örneğin, Terminal'de: export DB_PASSWORD='senin_mysql_parolan'
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'), # Veritabanı sunucusunun adresi
    'user': os.getenv('DB_USER', 'root'),     # MySQL kullanıcı adı
    'password': os.getenv('DB_PASSWORD', 'chapternesibe2003!'), # BURAYA KENDİ MYSQL ROOT PAROLANI YAZMALISIN!
    'database': os.getenv('DB_NAME', 'chapter_one_cafe_db') # Kullanılacak veritabanının adı
}

def get_db_connection():
    """MySQL veritabanına bir bağlantı kurar ve döndürür."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        # Veritabanı bağlantı hatası durumunda konsola hata mesajı yazdırır.
        print(f"Veritabanı bağlantı hatası: {err}")
        return None

@app.route('/', methods=['GET'])
def index_get():
    """Ana sayfa için GET isteğini işler. index.html dosyasını render eder."""
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register_book_club():
    """
    Book Club kayıt formundan gelen POST isteğini işler.
    Kullanıcı bilgilerini ve beklentilerini veritabanına kaydeder ve onay e-postası gönderir.
    """
    # Gelen isteğin JSON formatında olup olmadığını kontrol et.
    # Frontend JS kodun JSON gönderdiği için bu kısım çalışacak.
    if request.is_json:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        expectations = data.get('expectations')
    else:
        # JSON formatında gelmezse (örneğin normal bir HTML formu submit edilirse)
        name = request.form.get('name')
        email = request.form.get('email')
        expectations = request.form.get('expectations')

    # Gerekli tüm alanların doldurulup doldurulmadığını kontrol et.
    if not all([name, email, expectations]):
        return jsonify({"message": "Tüm alanlar doldurulmalıdır."}), 400

    # Veritabanı bağlantısı kur.
    conn = get_db_connection()
    if conn is None:
        return jsonify({"message": "Veritabanı bağlantısı kurulamadı."}), 500

    cursor = conn.cursor() # SQL sorgularını çalıştırmak için bir imleç oluştur.
    try:
        # 1. Kullanıcının (e-posta adresine göre) zaten var olup olmadığını kontrol et.
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        user_id = None

        if user:
            user_id = user[0] # Kullanıcı zaten varsa, mevcut ID'sini kullan.
        else:
            # Kullanıcı yoksa, 'users' tablosuna yeni bir kayıt ekle.
            # NOT: Formda parola alanı olmadığı için, password_hash sütununu NULL olarak ayarlıyoruz.
            # users tablosunda password_hash sütununun NULL değer kabul ettiğinden emin olmalısın.
            cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            user_id = cursor.lastrowid # Yeni eklenen kullanıcının ID'sini al.

        # 2. Kayıt işlemi için bir etkinlik ID'si belirle.
        # Senin HTML'inde etkinlik seçimi olmadığı için sabit bir ID kullanıyoruz.
        # Gerçek bir uygulamada, bu ID frontend'den gelmeli veya dinamik olarak belirlenmeli.
        event_id = 1 # Varsayılan etkinlik ID'si. Veritabanındaki 'events' tablosunda bu ID'ye sahip bir etkinlik olmalı.

        # 3. 'registrations' tablosuna yeni kaydı ekle.
        sql = "INSERT INTO registrations (user_id, event_id, expectations) VALUES (%s, %s, %s)"
        cursor.execute(sql, (user_id, event_id, expectations))
        conn.commit() # Veritabanındaki değişiklikleri kalıcı hale getir.

        # 4. Kayıt onay e-postası gönder.
        msg = Message(
            subject="Book Club Registration Confirmation",
            sender=app.config['MAIL_USERNAME'],
            recipients=[email]
        )
        msg.body = f"Hello {name},\n\nThank you for registering for the Book Club!\nWe received your expectations:\n{expectations}\n\nLooking forward to seeing you there!"

        try:
            mail.send(msg)
            print("Confirmation email sent successfully!") # Konsola başarı mesajı yazdır.
        except Exception as e:
            print(f"Failed to send confirmation email: {e}") # Konsola e-posta gönderme hatasını yazdır.

        # Frontend'e başarılı yanıt gönder.
        return jsonify({"message": "Kayıt başarılı! Teşekkürler."}), 200

    except mysql.connector.Error as err:
        conn.rollback() # Veritabanı hatası olursa yapılan değişiklikleri geri al.
        print(f"Veritabanı hatası: {err}")
        return jsonify({"message": f"Kayıt başarısız: {err}"}), 500 # Frontend'e hata mesajı gönder.
    except Exception as e:
        print(f"Genel hata: {e}") # Diğer tüm hataları yakala.
        return jsonify({"message": f"Bir hata oluştu: {e}"}), 500 # Frontend'e genel hata mesajı gönder.
    finally:
        # İşlem sonunda imleci ve bağlantıyı kapat.
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    # Flask uygulamasını başlat. Debug modu açık, bu geliştirme için iyidir.
    # Port 5001 olarak ayarlandı, çünkü frontend'deki fetch isteği bu porta gidiyor.
    app.run(debug=True, port=5001)
