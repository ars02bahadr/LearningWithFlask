# Flask Kullanıcı Yönetim Sistemi

Bu proje, Flask kullanılarak geliştirilmiş kapsamlı bir kullanıcı yönetim sistemidir. JWT tabanlı kimlik doğrulama, kullanıcı tipleri, roller ve profil yönetimi gibi temel özellikleri içerir.

## Özellikler

- 🔐 JWT tabanlı kimlik doğrulama
- 👥 Kullanıcı yönetimi (CRUD işlemleri)
- 📁 Profil fotoğrafı yükleme
- � Kullanıcı tipleri yönetimi
- ✨ Modern ve güvenli API tasarımı

## Proje Yapısı

```
app/
├── __init__.py
├── main.py              # Flask ana uygulama
├── database.py          # Veritabanı bağlantısı
├── auth/               # Kimlik doğrulama modülü
│   ├── __init__.py
│   ├── routes.py       # Auth endpoint'leri
│   ├── schemas.py      # Auth şemaları
│   └── views.py        # Auth iş mantığı
├── users/             # Kullanıcı modülü
│   ├── __init__.py
│   ├── models.py      # Kullanıcı modeli
│   ├── routes.py      # Kullanıcı endpoint'leri
│   ├── schemas.py     # Kullanıcı şemaları
│   └── views.py       # Kullanıcı iş mantığı
├── user_types/        # Kullanıcı tipleri modülü
│   ├── __init__.py
│   ├── models.py      # Kullanıcı tip modeli
│   ├── routes.py      # Kullanıcı tip endpoint'leri
│   ├── schemas.py     # Kullanıcı tip şemaları
│   └── views.py       # Kullanıcı tip iş mantığı
└── user_roles/        # Kullanıcı rolleri modülü
    ├── __init__.py
    ├── models.py      # Rol modeli
    ├── routes.py      # Rol endpoint'leri
    ├── schemas.py     # Rol şemaları
    └── views.py       # Rol iş mantığı
```

## Kurulum

1. Projeyi klonlayın:
```bash
git clone [proje-url]
cd [proje-dizini]
```

2. Sanal ortam oluşturun ve aktif edin:
```bash
python -m venv venv
# Windows için
venv\Scripts\activate
# Linux/Mac için
source venv/bin/activate
```

3. Gereksinimleri yükleyin:
```bash
pip install -r requirements.txt
```

4. Uygulamayı çalıştırın:
```bash
python main.py
```

## API Endpoint'leri

### Kimlik Doğrulama
- `POST /auth/login` - Kullanıcı girişi ve token alma

### Kullanıcılar
- `GET /users/get_all` - Tüm kullanıcıları listele
- `GET /users/get/<user_id>` - Belirli bir kullanıcıyı getir
- `POST /users/create` - Yeni kullanıcı oluştur
- `PUT /users/update` - Kullanıcı bilgilerini güncelle
- `DELETE /users/delete/<user_id>` - Kullanıcı sil

### Kullanıcı Tipleri
- `GET /user-types/get_all` - Tüm kullanıcı tiplerini listele
- `POST /user-types/create` - Yeni kullanıcı tipi oluştur
- `PUT /user-types/update` - Kullanıcı tipi güncelle
- `DELETE /user-types/delete/<type_id>` - Kullanıcı tipi sil

### Kullanıcı Rolleri
- `GET /user-roles/get_all` - Tüm rolleri listele
- `POST /user-roles/create` - Yeni rol oluştur
- `PUT /user-roles/update` - Rol güncelle
- `DELETE /user-roles/delete/<role_id>` - Rol sil

## Özellik Detayları

### Kullanıcı Yönetimi
- Profil fotoğrafı yükleme (JPEG, PNG, JPG)
- Çoklu rol atama
- Aktif/pasif kullanıcı durumu

### Güvenlik
- JWT tabanlı kimlik doğrulama
- Güvenli dosya yükleme kontrolleri
- Şifre hashleme
- Token süresi sınırlandırma (1 gün)

### Dosya Yönetimi
- Otomatik upload dizini oluşturma
- Güvenli dosya adı oluşturma
- Dosya boyutu ve tip kontrolü
- Statik dosya sunumu

## Teknik Detaylar

- Flask 2.0+
- Flask-RESTX (API ve Swagger UI)
- Flask-JWT-Extended
- SQLAlchemy
- SQLite veritabanı
- Swagger dokümantasyonu

## API Dokümantasyonu

API dokümantasyonuna aşağıdaki URL'den erişebilirsiniz:
- Swagger UI: `http://localhost:5000/`

## Geliştirme

1. Yeni bir özellik eklemek için:
   - İlgili modülde models.py'da modeli tanımlayın
   - schemas.py'da şemaları oluşturun
   - views.py'da iş mantığını yazın
   - routes.py'da endpoint'leri tanımlayın

2. Veritabanı değişiklikleri için:
   - models.py'da gerekli değişiklikleri yapın
   - Uygulamayı yeniden başlatın

## API Kullanımı

1. Kullanıcı girişi yapın:
```bash
curl -X POST "http://localhost:5000/auth/login" -H "Content-Type: application/json" -d '{"email":"your-email","password":"your-password"}'
```

2. Alınan token'ı diğer isteklerde kullanın:
```bash
curl -X GET "http://localhost:5000/users/get_all" -H "Authorization: Bearer your-token"
```

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
