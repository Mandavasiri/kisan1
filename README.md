# 🌾 Smart Crop Advisory System

> AI-Powered Farming Intelligence for Every Indian Farmer

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)
[![Languages](https://img.shields.io/badge/Languages-8-blue?style=flat)](app.py)
[![Modules](https://img.shields.io/badge/Modules-19-brightgreen?style=flat)](app.py)
[![Voice](https://img.shields.io/badge/Voice-Enabled-orange?style=flat)](app.py)
[![Weather](https://img.shields.io/badge/Weather-Live_API-0288d1?style=flat)](app.py)

---

## 🎬 Demo

> 🌐 **Live App:** [your-app.streamlit.app](https://your-app.streamlit.app)
>
> 🎥 **Demo Video:** [Add YouTube/Drive link here]

### Screenshots

| Dashboard | Crop Recommendation | Disease Scanner |
|-----------|---------------------|-----------------|
| ![Dashboard](screenshots/dashboard.png) | ![Crop](screenshots/crop_rec.png) | ![Disease](screenshots/disease.png) |

| Govt Schemes | Loan Calculator | AI Chatbot |
|--------------|-----------------|-----------|
| ![Schemes](screenshots/schemes.png) | ![Loan](screenshots/loan.png) | ![Chat](screenshots/chatbot.png) |

> 💡 Create a `screenshots/` folder and upload your app screenshots to make this README shine!

---

## 📖 About

Smart Crop Advisory is a full-stack AI agricultural platform built in Python + Streamlit.
It helps India's 140 million small and marginal farmers with multilingual, voice-enabled farming intelligence — completely free.

**Problem:** Small farmers lack access to expert advice, real-time market data, and government scheme information in their language.

**Solution:** One app. 19 modules. 8 languages. Voice enabled. Mobile friendly.

---

## ✨ 19 Modules

| Module | Description |
|--------|-------------|
| 🏠 Dashboard | Weather, market trends, crop calendar, alerts |
| 🌱 Crop Recommendation | AI crop selection: soil + climate + season |
| 🔬 Disease Scanner | Upload leaf photo → disease + treatment |
| 🌤️ Weather (Live API) | OpenWeatherMap live data + farming advisory |
| 📈 Market Prices | Mandi prices + 12-month trend charts |
| 💧 Irrigation Planner | Weekly irrigation schedule by soil/crop |
| 🧪 Fertilizer Guide | Precision NPK plan + application schedule |
| 🐛 Pest Warning | Seasonal alerts + IPM strategies |
| 🔄 Crop Rotation | 3-year rotation planner |
| 📚 Crop Library | Encyclopedia for 10+ crops |
| 🤖 AI Chatbot | Natural language farming assistant |
| 📊 Farm Analytics | Yield, disease, profitability charts |
| 🏛️ Govt Schemes | PM-KISAN, PMFBY, KCC + 5 more |
| 💰 Loan & Insurance | KCC eligibility + PMFBY calculator |
| 🛰️ Satellite Monitor | NDVI crop health map |
| 🚁 Drone Scout | Field inspection simulation |
| 💡 Daily Tips | 15+ farming tips by category |
| 📅 Seasonal Guide | Kharif / Rabi / Summer planning |
| 👥 About / Team | Project and team info |

---

## 🌐 8 Language Support + Voice

| Language | Voice Code |
|----------|-----------|
| English | en-IN |
| हिंदी Hindi | hi-IN |
| తెలుగు Telugu | te-IN |
| বাংলা Bengali | bn-IN |
| தமிழ் Tamil | ta-IN |
| मराठी Marathi | mr-IN |
| ಕನ್ನಡ Kannada | kn-IN |
| ગુજરાતી Gujarati | gu-IN |

Voice: Browser Web Speech API — no library needed. Best on Chrome Android.

---

## 🚀 Quick Start

```bash
git clone https://github.com/yourusername/smart-crop-advisory.git
cd smart-crop-advisory
pip install -r requirements.txt
streamlit run app.py
```

---

## ☁️ Deploy Free on Streamlit Cloud

1. Push repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo → set `app.py` → Deploy ✅

---

## 📁 Project Structure

```
smart-crop-advisory/
├── app.py                 # Main app (2800+ lines)
├── requirements.txt       # Dependencies
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── .gitignore
├── .streamlit/
│   └── config.toml        # Green theme config
├── data/
│   └── crop_dataset.csv   # Sample ML dataset (50 rows, 10 crops)
└── screenshots/           # Add your screenshots here
```

---

## 🌤️ Weather API Setup

1. Free signup at [openweathermap.org](https://openweathermap.org/api)
2. Copy API key → paste in app's Weather module
3. Works for any Indian city!

> No key? App shows realistic simulated weather as fallback.

---

## 🏷️ GitHub Topics to Add

```
python streamlit agriculture ai farmers india kisan
crop-recommendation disease-detection weather-api hackathon
smart-farming precision-agriculture hindi telugu
```

---

## 🤝 Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) — all contributions welcome!

---

## 📄 License

MIT — Free for education, research, and farmer welfare.

---

> *"When farmers prosper, the nation prospers."* 🇮🇳
> Built with ❤️ for India's farmers.
