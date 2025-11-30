# 🧠 Radyoloji Ses Dosyası Asistanı

Bu proje, içerisinde birden fazla hastaya ait karmaşık ve sırasız bilgiler içeren ses kayıtlarını analiz eden ve **her hasta için yapılandırılmış (JSON formatında) raporlar üreten yapay zeka tabanlı bir agent sistemidir.**

---

## 🎯 Projenin Amacı

Tıbbi ortamlarda doktorlar genellikle vizit sonrası notlarını uzun bir ses kaydına dikte ederler.  
Bu dikteler sırasında:
- Birden fazla hastadan bahsedilebilir,  
- Farklı hastaların bilgileri birbirine karışabilir,  
- Daha önce bahsedilen bir hastaya “geri dönüş” yapılabilir.  

Bu **karmaşık ve doğrusal olmayan** ses kayıtlarını manuel olarak deşifre etmek oldukça zaman alıcıdır.  
Bu proje, bu süreci **otomatik hale getirerek**, tek bir ses kaydından **hasta bazında ayrıştırılmış, sınıflandırılmış ve yapılandırılmış tıbbi raporlar** üretmeyi hedefler.

---

## 🚀 Öne Çıkan Özellikler

- **🎧 Tek Ses Dosyasından Çoklu Rapor:**  
  Birden fazla hastanın bilgisini içeren tek bir uzun ses dosyasını işleyebilir.

- **🌐 Web Arayüzü (Spring Boot):**
  Kullanıcı dostu arayüz üzerinden ses dosyası yükleme ve sonuç görüntüleme.

- **🔊 Geniş Format Desteği:**
  MP3, OGG, WAV ve diğer yaygın ses formatlarını destekler.

- **🧩 Akıllı Gruplama:**  
  Aynı hastaya ait, farklı yerlerde bahsedilen bilgileri birleştirir.

- **🤖 Agent Mimarisi (2 Aşamalı):**  
  - **Orkestratör Agent:** Hastaları tespit eder ve transkripti anlamlı bloklara ayırır.  
  - **Rapor Üretme Agent’ı (LangGraph):** Her metin bloğunu detaylı işleyip yapılandırılmış veriye dönüştürür.

- **🩸 Otomatik Sınıflandırma:**  
  Her hasta raporunun türünü (örneğin *Toraks*, *Batın*, *Beyin*, *Lomber*, *Ayak Bileği* vb.) içerik analizine göre belirler.

- **🧱 Yapısal Veri Çıktısı:**  
  Pydantic şemalarıyla tutarlı ve temiz JSON formatı üretir.

- **📁 Hasta Bazında Çıktı:**  
  Her hasta için ayrı `.json` dosyası oluşturur.

---

## 🧬 Mimari ve İş Akışı

```text
    ┌─────────────────────────┐
    │  Web Arayüzü / Upload   │
    └───────────┬─────────────┘
                │
                ▼
    ┌─────────────────────────┐
    │  Backend (Spring Boot)  │
    └───────────┬─────────────┘
                │
                ▼
┌───────────────────────────────┐
│ 1. Ses-Metin Çevrimi (S2T)    │
│   (Hugging Face Whisper API)  │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│ 2. Orkestratör Agent (LLM)    │
│   - Hastaları Tespit Et       │
│   - Metinleri Grupla          │
└───────────────┬───────────────┘
                │ (Hasta A Metni), (Hasta B Metni), ...
                │
                ▼ (Her hasta metni için döngü)
╔══════════════════════════════════════════════════════════════════════════════╗
║ 3. Rapor Üretme Agent'ı (LangGraph ile kuruldu)                              ║
║                                                                              ║
║      ┌──────────────────┐                                                    ║
║      │ Router (LLM)     │--> 'toraks', 'kontrast_toraks', 'ust_batin',       ║
║      └────────┬─────────┘    'alt_batin', 'ayak_bilek', 'beyin', 'lomber'    ║
║               │ (Koşullu Yönlendirme)                                        ║
║               ▼                                                              ║
║       ┌────────────────┐                                                     ║
║       │ İlgili Form    │                                                     ║
║       │  Veri Çıkarıcı │                                                     ║
║       │ (LLM + Şema)   │                                                     ║
║       └───────┬────────┘                                                     ║
║               │                                                              ║
║               └                                                              ║
║               ▼                                                              ║
║      ┌──────────────────┐                                                    ║
║      │ Yapısal JSON Veri│                                                    ║
║      └──────────────────┘                                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
                │
                ▼
┌───────────────────────────────┐
│  Hasta_A.json, Hasta_B.json   │
└───────────────────────────────┘
```

## 🏗️ Teknoloji Mimarisi

| Katman | Teknoloji / Kütüphane |
|--------|------------------------|
| **Frontend & Backend** | Java Spring Boot, Thymeleaf, Bootstrap |
| **Orkestrasyon & Agent Mantığı** | Python, LangChain, LangGraph |
| **Dil Modelleri (LLM)** | Google Gemini Pro |
| **Ses-Metin Çevrimi (S2T)** | Hugging Face Whisper |
| **Veri Yapılandırma (Schema)** | Pydantic |

---

## ⚙️ Kurulum

### 1. Projeyi Klonlayın
```bash
git clone https://github.com/bedirhan420/radiology_assistant.git
cd radiology_assistant
```

### 2. Python Ortamını Hazırlayın (AI Modülü)
```bash
# Conda ortamı oluşturun
conda create -n radiology_assistant python=3.12.11
conda activate radiology_assistant

# Bağımlılıkları yükleyin
cd ai
pip install -r requirements.txt
cd ..
```

### 3. API Anahtarlarını Ayarlayın
Ana dizinde `.env` dosyası oluşturun ve aşağıdaki içeriği ekleyin:

```bash
# Google AI Studio'dan alınacak: https://aistudio.google.com/app/apikey
GOOGLE_API_KEY="BURAYA_GOOGLE_API_ANAHTARINIZI_YAPISTIRIN"

# Hugging Face'ten alınacak: https://huggingface.co/settings/tokens
HF_TOKEN="hf_BURAYA_HUGGINGFACE_TOKENINI_YAPISTIRIN"
```

### 4. Backend (Spring Boot) Çalıştırın
```bash
cd backend
mvn spring-boot:run
```
Uygulama `http://localhost:8080` adresinde çalışacaktır.

---

# 🧩 Nasıl Kullanılır?

1. Tarayıcınızda `http://localhost:8080` adresine gidin.
2. "Ses Dosyası Seçin" butonuna tıklayarak bilgisayarınızdan bir ses dosyası (.mp3, .ogg vb.) seçin.
3. "Yükle ve Dönüştür" butonuna tıklayın.
4. İşlem tamamlandığında sonuç ekranda görüntülenecektir.

Alternatif olarak Python modülünü doğrudan komut satırından da çalıştırabilirsiniz:
```bash
python ai/src/orchestrator.py --audio_file data/audio/sizin_ses_dosyaniz.mp3
```

---

# 📂 Dosya Yapısı

```text
/radiology_assistant/
│-- .env
│-- README.md
│
│-- /ai/ (Python AI Modülü)
│   │-- requirements.txt
│   │-- /data/
│   │-- /src/
│       │-- /graph/
│       │-- /schemas/
│       │-- /tools/
│       │-- config.py
│       │-- orchestrator.py
│       │-- main.py
│
│-- /backend/ (Java Spring Boot)
│   │-- pom.xml
│   │-- /src/
│       │-- /main/
│           │-- /java/
│           │-- /resources/
│               │-- /static/css/
│               │-- /templates/
```