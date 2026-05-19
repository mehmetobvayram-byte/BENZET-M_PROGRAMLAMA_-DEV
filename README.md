<<<<<<< HEAD
# 🚗 Akıllı Oto Yıkama Kapasite Analizi ve Simülasyon Sistemi

Bu proje, bir oto yıkama istasyonunun günlük iş akışını, araç yoğunluğunu ve personel verimliliğini analiz etmek amacıyla geliştirilmiş, yüksek sadakatli bir simülasyon ve dashboard sistemidir.

## 👤 Proje Sahibi
- **İsim:** Mehmet Özbayram
- **Okul No:** 22430070049

---

## 🎯 Projenin Amacı
İşletme sahiplerinin ve sistem analistlerinin; yıkama kabini sayısı, personel sayısı ve araç geliş sıklığı gibi parametrelerin müşteri bekleme süreleri üzerindeki etkisini gözlemlemesini sağlamaktır. Sistem, darboğazları (bottleneck) tespit ederek operasyonel verimliliği artırmak için somut veriler sunar.

## 🚀 Öne Çıkan Özellikler ve Yapılan Geliştirmeler

Başlangıçta temel bir yıkama modeli olan proje, süreç içerisinde aşağıdaki gelişmiş özelliklerle donatılmıştır:

### 1. Özelleştirilmiş Araç Kategorileri
Sistem artık sadece "araç" değil, farklı fiziksel özelliklere ve işlem sürelerine sahip 5 farklı kategoriyi simüle eder:
- **Küçük Araçlar:** Motor ve Otomobil (Hızlı işlem süresi).
- **Büyük Araçlar:** Otobüs ve Tır (Uzun işlem süresi).
- **Görevli Araçlar:** Ambulans, İtfaiye vb. (Özel öncelik ve kabin).

### 2. Akıllı Kabin Yönetimi
Araç tiplerine göre 3 farklı kabin grubu tanımlanmıştır:
- **Küçük Araç Kabinleri:** Sadece Motor ve Otomobiller için.
- **Büyük Araç Kabinleri:** Sadece Otobüs ve Tırlar için.
- **Görevli Araç Kabinleri:** Sadece Görevli Araçlar için.

### 3. Detaylı Metrik Analizi
Genel ortalamalar yerine, her araç grubu için **Yıkama** ve **Kurulama** bekleme süreleri ayrı ayrı hesaplanır. Bu sayede hangi araç tipinin nerede daha çok beklediği net bir şekilde görülebilir.

### 4. Canlı Takip Dashboard'u
- **Glassmorphism Tasarım:** Modern, şık ve göz yormayan karanlık mod arayüzü.
- **Gerçek Zamanlı Görselleştirme:** Araçların kuyruğa girişi, kabinlere dağılımı ve personel tarafından kurulanma süreçleri anlık animasyonlarla takip edilebilir.
- **Dinamik Log Sistemi:** Yaşanan her olay (varış, yıkama bitişi, ayrılış) zaman damgasıyla birlikte ekrana akar.

## 🛠 Kullanılan Teknolojiler
- **Python (SimPy):** Matematiksel ve istatistiksel simülasyon motoru.
- **Flask:** Backend API ve web sunucusu.
- **HTML5 & CSS3:** Modern UI tasarımı (Gradient, Flexbox, Grid).
- **JavaScript (ES6+):** Canlı veri işleme ve DOM manipülasyonu.
- **FontAwesome:** Dinamik araç ve durum ikonları.


=======
# Oto Yıkama Kapasite Analizi ve Simülasyon Sistemi - Proje Raporu

**Projenin Amacı ve Çıkış Noktası**
Bu projeyi geliştirirken temel amacım, bir oto yıkama istasyonunun günlük iş akışını gerçekçi bir şekilde modellemek ve olası darboğazları (bottleneck) tespit edebileceğim görsel bir kapasite analiz aracı ortaya koymaktı. Tesise gelen araç yoğunluğu, yıkama kabinlerinin sayısı ve kurulama personelinin verimliliği gibi değişkenlerin müşteri bekleme sürelerine etkisini analiz edebileceğim interaktif bir simülasyon ortamı yaratmayı hedefledim.

**Kullanılan Teknolojiler ve Mimari**
Altyapıyı geliştirirken işin hem matematiksel (istatistiksel) simülasyon tarafına hem de son kullanıcı için görselleştirme tarafına eşit derecede önem verdim:
- **SimPy (Python):** Arka planda simülasyon motoru olarak SimPy kütüphanesini kullandım. Araçların tesise rastgele aralıklarla varışı, yıkama kuyruğunda beklemesi, yıkanması ve ardından kurulama personeli tarafından temizlenip sistemden çıkışına kadar devam eden "kesikli olay simülasyonunu (discrete-event simulation)" bu sayede modelledim.
- **Flask:** Backend ile frontend'in köprüsü olarak Flask'ı seçtim. SimPy'ın ürettiği veriyi (kuyruk süreleri, tamamlanan araç sayısı ve olay logları) alıp JSON formatında arayüze servis eden esnek bir web sunucusu yazdım.
- **Modern ve Dinamik Frontend (HTML/CSS/JS):** Sadece kuru veriler okumak yerine, sürecin adeta gözlerimin önünde yaşanabileceği bir arayüz istedim. Glassmorphism (cam efekti) efektleri ve degrade renkler (gradient) kullanarak modern bir tasarım oluşturup HTML/CSS ile UI hazırladım. JavaScript kullanarak, saniyeler içinde arka planda hesaplanıp biten tüm 4 saatlik simülasyon verilerini adım adım okuyarak, izleyiciye seçilen bir oynatma hızında "canlı simülasyon" izlenimi veren bir interaktif Dashboard kodladım.

**Sistemin Çalışma Mantığı**
Hazırladığım kontrol paneli üzerinden yıkama kabini sayısını, kurulama personel sayısını ve potansiyel müşteri geliş sıklığını manuel olarak ayarlayabiliyorum. Parametreleri belirleyip simülasyonu başlattığımda:
1. Python/SimPy tarafı bu senaryoyu milisaniyeler içinde koşturup yaşanan tüm olayları bir zaman çizelgesine döküyor.
2. Arayüz bu veriyi aldığında bir "yeniden oynatma (playback)" fonksiyonu devreye giriyor. 
3. Araçların bekleme sırasına girmesi, kabinlerin dolup boşalması, personel atamaları dinamik CSS ve JS animasyonlarıyla ekrana yansıtılıyor ve canlı bir log ekranından anlık olarak okunabiliyor.

**Elde Ettiğim Çıktılar ve Sonuç**
Projenin sonunda, bir işletmenin iş akışını ve müşteri memnuniyetini doğrudan etkileyen unsurları somut verilere dayanarak inceleme şansına sahip oldum. Örneğin; sadece yıkama kabini sayısını artırmanın kuyrukları önlemek için yetersiz kaldığı, aynı oranda kurulama personeli atanmazsa darboğazın sadece "kurulama kuyruğuna" taşınacağı gerçeğini gözlemleyebildim. 

Sonuç olarak; hem çeşitli parametre denemeleri yapabildiğim hem metrikleri analiz edebildiğim hem de sürecin animasyonlu özetini takip edebildiğim, vizyonuma uygun, son derece şık ve işlevsel bir sistem kurmuş oldum.
>>>>>>> aabd3721211c5c39aec6db98f05a32c2411c65e2
