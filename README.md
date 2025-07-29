# AI-Budget-Planner

🤖 Yapay Zeka Destekli Bütçe Planlayıcısı

## 🚀 Özellikler

- 💰 Gelir-gider takibi
- 📊 Görsel grafikler ve analizler
- 🤖 AI destekli bütçe önerileri
- 🎨 Modern ve kullanıcı dostu arayüz
- 🔄 Gerçek zamanlı hesaplamalar
- 📈 Tasarruf hedefi takibi
- 🎯 Gelecek planlama

## 🛠️ Teknolojiler

- **Frontend**: Streamlit
- **Backend**: Flask
- **Veri Görselleştirme**: Plotly
- **AI**: OpenAI API
- **Veritabanı**: SQLAlchemy (gelecek sürümlerde)

## 📦 Kurulum

1. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

2. **Backend'i başlatın:**
```bash
cd backend
python app.py
```

3. **Frontend'i başlatın (yeni terminal):**
```bash
cd frontend
streamlit run app.py
```

## 🎯 Kullanım

1. **Sidebar'dan gelir ve gider bilgilerinizi girin**
   - Aylık gelirinizi belirleyin
   - Kategori bazlı giderlerinizi girin

2. **Otomatik hesaplamaları görün**
   - Kalan bütçe
   - Tasarruf oranı
   - Toplam gider analizi

3. **AI önerilerini alın**
   - "🤖 AI Önerileri Al" butonuna tıklayın
   - Kişiselleştirilmiş tasarruf önerileri

4. **Grafikleri inceleyin**
   - Gider dağılımı (pasta grafik)
   - Gelir vs Gider analizi (bar grafik)

## 🔌 API Endpoints

- `GET /` - Ana sayfa
- `GET /health` - Sağlık kontrolü
- `POST /analyze` - Bütçe analizi
- `GET /budget` - Bütçe verileri
- `GET /suggestions` - Genel öneriler

## 📊 Bütçe Kategorileri

- 🏠 **Konut**: Kira, ev kredisi, bakım
- 🍽️ **Yemek**: Market, restoran, kafeler
- 🚗 **Ulaşım**: Benzin, toplu taşıma, taksi
- 💡 **Faturalar**: Elektrik, su, internet, telefon
- 🎬 **Eğlence**: Film, konser, hobi
- 💎 **Tasarruf**: Birikim, yatırım
- 📦 **Diğer**: Sağlık, eğitim, giyim

## 🤖 AI Önerileri

Sistem şu kriterlere göre öneriler sunar:

- **Tasarruf Oranı**: %20'nin altındaysa uyarı
- **Bütçe Açığı**: Gelirden fazla harcama varsa uyarı
- **Konut Oranı**: Gelirin %30'unu aşarsa öneri
- **Yemek Oranı**: Gelirin %15'ini aşarsa öneri
- **Acil Durum Fonu**: 3-6 aylık gider için öneri

## 🎨 Arayüz Özellikleri

- **Responsive Tasarım**: Tüm cihazlarda uyumlu
- **Modern UI**: Temiz ve kullanıcı dostu
- **Renk Kodlaması**: 
  - 🟢 Yeşil: Sağlıklı bütçe
  - 🟡 Sarı: Dikkat gerektiren durum
  - 🔴 Kırmızı: Kritik durum

## 🚀 Gelecek Özellikler

- [ ] Veritabanı entegrasyonu
- [ ] Kullanıcı hesapları
- [ ] Geçmiş veri analizi
- [ ] Mobil uygulama
- [ ] Daha gelişmiş AI önerileri
- [ ] Bütçe hatırlatıcıları

## 🐛 Sorun Giderme

**Backend bağlantı hatası:**
```bash
# Backend'in çalıştığından emin olun
cd backend
python app.py
```

**Port çakışması:**
```bash
# Farklı port kullanın
export PORT=5001
python app.py
```

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 👥 Geliştirici

Bu proje, finansal farkındalığı artırmak ve tasarruf hedeflerine ulaşmayı kolaylaştırmak için geliştirilmiştir.

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!